"""
Prompt builder for the AI Meal Plan Generator.
Constructs a deterministic, structured prompt from user data.
"""
import json


def build_meal_plan_prompt(user_data: dict, nutrition_context: list) -> str:
    """
    Build a structured prompt for Gemini to generate a 7-day meal plan.

    Args:
        user_data: Dict with age, gender, height_cm, weight_kg, goal, activity_level,
                   food_preference, allergies, country, cuisine, budget_per_day_usd,
                   workout_time, target_calories, target_protein_g, target_carbs_g, target_fat_g.
        nutrition_context: List of food dicts from the local nutrition DB to ground responses.

    Returns:
        A multi-line prompt string.
    """
    foods_str = json.dumps(nutrition_context[:30], indent=2)  # limit context size

    goal_descriptions = {
        'lose_fat': 'fat loss (caloric deficit, high protein, lower carbs)',
        'build_muscle': 'muscle building (caloric surplus, high protein, moderate carbs)',
        'maintain': 'maintenance (balanced macros)',
        'improve_health': 'general health improvement (whole foods, high fiber)',
        'increase_endurance': 'endurance training (high carbs, moderate protein)',
    }
    goal_desc = goal_descriptions.get(user_data.get('goal', 'maintain'), 'balanced diet')

    allergies = user_data.get('allergies', [])
    allergy_str = ', '.join(allergies) if allergies else 'None'

    prompt = f"""You are a certified dietitian and nutrition expert. Generate a structured 7-day meal plan.

## User Profile
- Age: {user_data.get('age', 'Unknown')}
- Gender: {user_data.get('gender', 'Not specified')}
- Height: {user_data.get('height_cm', '?')} cm
- Weight: {user_data.get('weight_kg', '?')} kg
- Goal: {goal_desc}
- Activity Level: {user_data.get('activity_level', 'moderate')}
- Food Preference: {user_data.get('food_preference', 'none')}
- Allergies / Restrictions: {allergy_str}
- Country: {user_data.get('country', 'International')}
- Cuisine Preference: {user_data.get('cuisine_preference', 'Mixed')}
- Daily Budget: ${user_data.get('budget_per_day_usd', 15)} USD
- Workout Time: {user_data.get('workout_time', 'Morning')}

## Daily Targets
- Calories: {user_data.get('target_calories', 2000)} kcal
- Protein: {user_data.get('target_protein_g', 150)}g
- Carbs: {user_data.get('target_carbs_g', 200)}g
- Fat: {user_data.get('target_fat_g', 65)}g
- Water: {user_data.get('water_intake_ml', 2500)}ml

## Available Foods from Nutrition Database (use these when possible)
{foods_str}

## Instructions
1. Create a 7-day meal plan (day_1 through day_7).
2. Each day must have: breakfast, lunch, dinner, and at least one snack.
3. Include prep_time_minutes and cook_time_minutes for each meal.
4. Never include allergens: {allergy_str}.
5. Respect the food preference: {user_data.get('food_preference', 'none')}.
6. Keep each meal's calories realistic and the daily total close to the target.
7. Include a grocery_list array at the root with all ingredients needed for the full week.
8. The grocery_list items must have: name, quantity (number), unit (string), category.

## Required JSON Output Format
Return ONLY valid JSON with this exact structure:
{{
  "plan_title": "string",
  "total_days": 7,
  "daily_targets": {{
    "calories": number,
    "protein_g": number,
    "carbs_g": number,
    "fat_g": number,
    "water_ml": number
  }},
  "days": [
    {{
      "day_number": 1,
      "day_name": "Monday",
      "total_calories": number,
      "total_protein_g": number,
      "total_carbs_g": number,
      "total_fat_g": number,
      "meals": [
        {{
          "meal_type": "breakfast|lunch|dinner|snack|pre_workout|post_workout",
          "name": "string",
          "description": "string",
          "calories": number,
          "protein_g": number,
          "carbs_g": number,
          "fat_g": number,
          "prep_time_minutes": number,
          "cook_time_minutes": number,
          "recipe_steps": "string with step-by-step instructions",
          "ingredients": ["ingredient 1", "ingredient 2"]
        }}
      ]
    }}
  ],
  "grocery_list": [
    {{
      "name": "string",
      "quantity": number,
      "unit": "string",
      "category": "string"
    }}
  ],
  "notes": "Any important nutritional notes or tips for this plan."
}}
"""
    return prompt
