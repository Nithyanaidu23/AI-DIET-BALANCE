"""AI Engine views — meal plan generation."""
import logging
from datetime import date, timedelta

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from health.calculators import full_health_report
from mealplanner.models import MealPlan, Meal, GroceryItem
from mealplanner.serializers import MealPlanSerializer
from nutrition.models import Food
from nutrition.serializers import FoodMiniSerializer
from users.models import UserProfile

from .gemini_client import call_gemini
from .prompt_builder import build_meal_plan_prompt
from .response_parser import validate_and_parse, ValidationError

logger = logging.getLogger('ai_engine')


class GenerateMealPlanView(APIView):
    """
    POST /api/generate-plan/
    Full orchestration: profile → calcs → Gemini → parse → save → return.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)

        # ── 1. Gather inputs (request body overrides profile) ──────────────────
        def get(key, default=None):
            return request.data.get(key) or getattr(profile, key, None) or default

        weight_kg = float(get('weight_kg') or profile.weight_kg or 70)
        height_cm = float(get('height_cm') or profile.height_cm or 170)
        age = int(get('age') or profile.age or 25)
        gender = get('gender') or profile.gender or 'male'
        activity_level = get('activity_level') or profile.activity_level or 'moderate'
        goal = get('goal') or profile.fitness_goal or 'maintain'
        food_preference = get('food_preference') or profile.food_preference or 'none'
        allergies = profile.allergies_list if hasattr(profile, 'allergies_list') else []
        country = get('country') or profile.country or ''
        cuisine = get('cuisine_preference') or profile.cuisine_preference or ''
        budget = float(get('budget_per_day_usd') or profile.budget_per_day_usd or 15)
        workout_time = get('workout_time') or profile.workout_time or 'Morning'

        # ── 2. Calculate targets via deterministic formulas ────────────────────
        health = full_health_report(weight_kg, height_cm, age, gender, activity_level, goal)

        # ── 3. Pull nutrition context from local DB ────────────────────────────
        food_qs = Food.objects.all()
        if food_preference == 'vegetarian':
            food_qs = food_qs.filter(is_vegetarian=True)
        elif food_preference == 'vegan':
            food_qs = food_qs.filter(is_vegan=True)

        foods = FoodMiniSerializer(food_qs[:30], many=True).data

        # ── 4. Build prompt ────────────────────────────────────────────────────
        user_data = {
            'age': age, 'gender': gender, 'height_cm': height_cm, 'weight_kg': weight_kg,
            'goal': goal, 'activity_level': activity_level, 'food_preference': food_preference,
            'allergies': allergies, 'country': country, 'cuisine_preference': cuisine,
            'budget_per_day_usd': budget, 'workout_time': workout_time,
            'target_calories': int(health['goal_calories']),
            'target_protein_g': int(health['protein_g']),
            'target_carbs_g': int(health['carbs_g']),
            'target_fat_g': int(health['fat_g']),
            'water_intake_ml': health['water_intake_ml'],
        }

        prompt = build_meal_plan_prompt(user_data, list(foods))

        # ── 5. Call Gemini ─────────────────────────────────────────────────────
        try:
            raw_response = call_gemini(prompt)
        except (ValueError, RuntimeError) as exc:
            logger.error('Gemini call failed: %s', exc)
            log_event(user, 'MEAL_GENERATION_FAILED', {'error': str(exc), 'stage': 'gemini_api_call'})
            return Response(
                {'error': str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # ── 6. Validate & parse response ───────────────────────────────────────
        try:
            parsed = validate_and_parse(raw_response)
        except ValidationError as exc:
            logger.error('Meal plan validation error: %s', exc)
            log_event(user, 'MEAL_GENERATION_FAILED', {'error': str(exc), 'stage': 'validation'})
            return Response(
                {'error': f'AI returned an invalid meal plan: {exc}'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )


        # ── 7. Persist to database ─────────────────────────────────────────────
        today = date.today()
        targets = parsed['daily_targets']

        meal_plan = MealPlan.objects.create(
            user=user,
            title=parsed['plan_title'],
            start_date=today,
            end_date=today + timedelta(days=6),
            target_calories=targets['calories'],
            target_protein_g=targets['protein_g'],
            target_carbs_g=targets['carbs_g'],
            target_fat_g=targets['fat_g'],
            target_water_ml=targets['water_ml'],
            ai_generated=True,
            ai_prompt_summary=f'Goal: {goal} | Pref: {food_preference} | Cal: {targets["calories"]}',
            notes=parsed.get('notes', ''),
        )

        for day in parsed['days']:
            for meal_data in day['meals']:
                Meal.objects.create(
                    meal_plan=meal_plan,
                    day_number=day['day_number'],
                    meal_type=meal_data['meal_type'],
                    name=meal_data['name'],
                    description=meal_data['description'],
                    calories=meal_data['calories'],
                    protein_g=meal_data['protein_g'],
                    carbs_g=meal_data['carbs_g'],
                    fat_g=meal_data['fat_g'],
                    prep_time_minutes=meal_data.get('prep_time_minutes'),
                    cook_time_minutes=meal_data.get('cook_time_minutes'),
                    recipe_steps=meal_data.get('recipe_steps', ''),
                )

        # Save grocery list
        for item in parsed.get('grocery_list', []):
            GroceryItem.objects.create(
                meal_plan=meal_plan,
                name=item['name'],
                quantity=item['quantity'],
                unit=item['unit'],
                category=item['category'],
            )

        # ── 8. Log activity & return the full plan ───────────────────────────
        from activity_logs.signals import log_activity, log_event
        from activity_logs.models import ActionType
        ip = getattr(request, 'audit_meta', {}).get('ip', '')
        log_activity(user, ActionType.MEAL_GENERATED, description=f"Generated meal plan: {parsed['plan_title']} ({targets['calories']} kcal)", ip_address=ip)
        log_event(user, 'MEAL_GENERATED', raw_response.get('_telemetry', {}))


        serializer = MealPlanSerializer(meal_plan, context={'request': request})
        return Response(
            {
                'message': 'Meal plan generated and saved successfully.',
                'health_report': health,
                'meal_plan': serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
