"""Master API URL router — aggregates all app URLs under /api/."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from nutrition.views import FoodViewSet

router = DefaultRouter()
router.register('foods', FoodViewSet, basename='food')

urlpatterns = [
    # Auth
    path('', include('accounts.urls')),

    # User profile
    path('', include('users.urls')),

    # Nutrition DB
    path('', include(router.urls)),

    # Meal planner
    path('', include('mealplanner.urls')),

    # Health calculators + dashboard
    path('', include('health.urls')),

    # AI engine
    path('', include('ai_engine.urls')),

    # Audit logs and Exports
    path('', include('activity_logs.urls')),
]
