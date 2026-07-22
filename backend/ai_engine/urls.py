from django.urls import path
from .views import GenerateMealPlanView

urlpatterns = [
    path('generate-plan/', GenerateMealPlanView.as_view(), name='generate-plan'),
]
