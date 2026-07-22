"""Health app views — BMI, calorie calculator, dashboard, water tracker."""
from datetime import date, timedelta
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from mealplanner.models import MealPlan
from users.models import UserProfile
from .calculators import full_health_report
from .models import BMIRecord, WaterTracker
from .serializers import BMIInputSerializer, BMIRecordSerializer, WaterTrackerSerializer


class BMICalculatorView(APIView):
    """
    POST /api/bmi/
    Calculate BMI, body fat, ideal weight, macros, and water intake.
    Optionally saves a BMIRecord to track progress over time.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = BMIInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        report = full_health_report(
            weight_kg=data['weight_kg'],
            height_cm=data['height_cm'],
            age=data['age'],
            gender=data['gender'],
            activity_level=data['activity_level'],
            goal=data['goal'],
        )

        if data.get('save_record', True):
            BMIRecord.objects.create(
                user=request.user,
                weight_kg=data['weight_kg'],
                height_cm=data['height_cm'],
                bmi=report['bmi'],
                bmi_category=report['bmi_category'],
                body_fat_percent=report['body_fat_percent'],
                ideal_weight_kg=report['ideal_weight_kg'],
                goal_calories=report['goal_calories'],
            )

        from activity_logs.signals import log_activity
        from activity_logs.models import ActionType
        ip = getattr(request, 'audit_meta', {}).get('ip', '')
        log_activity(request.user, ActionType.BMI_CALCULATED, description=f"BMI: {report['bmi']} ({report['bmi_category']})", ip_address=ip)

        return Response(report)


class CalorieCalculatorView(APIView):
    """
    POST /api/calorie/
    Lightweight calorie-only calculation endpoint (no record saving).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = BMIInputSerializer(data={**request.data, 'save_record': False})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        report = full_health_report(**{k: data[k] for k in ['weight_kg', 'height_cm', 'age', 'gender', 'activity_level', 'goal']})
        return Response(report)


class BMIHistoryView(generics.ListAPIView):
    """GET /api/bmi/history/ — Past BMI records for progress charts."""
    serializer_class = BMIRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        days = int(self.request.query_params.get('days', 90))
        since = date.today() - timedelta(days=days)
        return BMIRecord.objects.filter(user=self.request.user, recorded_at__date__gte=since)


class WaterTrackerView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/water/ — Today's water log."""
    serializer_class = WaterTrackerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        target_ml = 2500
        if profile.weight_kg:
            from .calculators import recommended_water_intake_ml
            target_ml = recommended_water_intake_ml(
                float(profile.weight_kg),
                profile.activity_level or 'moderate'
            )
        obj, _ = WaterTracker.objects.get_or_create(
            user=self.request.user,
            date=date.today(),
            defaults={'target_ml': target_ml},
        )
        return obj

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        response = super().update(request, *args, **kwargs)
        from activity_logs.signals import log_activity
        from activity_logs.models import ActionType
        ip = getattr(request, 'audit_meta', {}).get('ip', '')
        log_activity(request.user, ActionType.WATER_UPDATED, description=f"Water updated: {request.data.get('amount_ml')}ml", ip_address=ip)
        return response


class DashboardView(APIView):
    """
    GET /api/dashboard/
    Aggregated data for the main dashboard page.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)

        # Latest BMI record
        latest_bmi = BMIRecord.objects.filter(user=user).first()
        bmi_data = BMIRecordSerializer(latest_bmi).data if latest_bmi else None

        # Water today
        water_today, _ = WaterTracker.objects.get_or_create(
            user=user, date=date.today(), defaults={'target_ml': 2500}
        )

        # Most recent meal plan
        latest_plan = MealPlan.objects.filter(user=user).prefetch_related('meals').first()
        from mealplanner.serializers import MealPlanSerializer
        plan_data = MealPlanSerializer(latest_plan, context={'request': request}).data if latest_plan else None

        # BMI 30-day trend
        since = date.today() - timedelta(days=30)
        bmi_trend = list(
            BMIRecord.objects.filter(user=user, recorded_at__date__gte=since)
            .values('recorded_at__date', 'bmi', 'weight_kg')
            .order_by('recorded_at__date')
        )

        return Response({
            'user': {
                'email': user.email,
                'full_name': user.full_name,
            },
            'profile': {
                'fitness_goal': profile.fitness_goal,
                'activity_level': profile.activity_level,
                'is_complete': profile.is_complete,
            },
            'latest_bmi': bmi_data,
            'water_today': WaterTrackerSerializer(water_today).data,
            'latest_meal_plan': plan_data,
            'bmi_trend': bmi_trend,
            'total_plans': MealPlan.objects.filter(user=user).count(),
        })


import sys
from django.db import connection


class SystemStatusView(APIView):
    """
    GET /api/health/status/
    Production monitoring check endpoint for UptimeRobot / Sentry / Prometheus.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        db_healthy = True
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            db_healthy = False

        return Response({
            'status': 'healthy' if db_healthy else 'degraded',
            'database_connected': db_healthy,
            'python_version': sys.version,
            'service': 'AI Diet Planner SaaS Backend',
        })

