from django.urls import path
from .views import BMICalculatorView, CalorieCalculatorView, BMIHistoryView, WaterTrackerView, DashboardView, SystemStatusView

urlpatterns = [
    path('health/status/', SystemStatusView.as_view(), name='health-status'),
    path('bmi/', BMICalculatorView.as_view(), name='bmi-calculate'),
    path('bmi/history/', BMIHistoryView.as_view(), name='bmi-history'),
    path('calorie/', CalorieCalculatorView.as_view(), name='calorie-calculate'),
    path('water/', WaterTrackerView.as_view(), name='water-tracker'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]

