from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MealPlanViewSet, FavoriteMealListView, GroceryItemUpdateView

router = DefaultRouter()
router.register('meal-plans', MealPlanViewSet, basename='meal-plan')

urlpatterns = [
    path('', include(router.urls)),
    path('favorites/', FavoriteMealListView.as_view(), name='favorites'),
    path('grocery/<int:pk>/', GroceryItemUpdateView.as_view(), name='grocery-item'),
]
