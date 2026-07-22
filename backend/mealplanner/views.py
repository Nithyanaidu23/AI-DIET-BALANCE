"""Views for the meal planner app."""
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MealPlan, FavoriteMeal, GroceryItem
from .serializers import (
    MealPlanSerializer,
    MealPlanListSerializer,
    GroceryItemSerializer,
    FavoriteMealSerializer,
)


class MealPlanViewSet(viewsets.ModelViewSet):
    """
    CRUD for meal plans.
    GET    /api/meal-plans/         — User's meal plan history.
    POST   /api/meal-plans/         — Create a manual plan.
    GET    /api/meal-plans/{id}/    — Detail view.
    PUT    /api/meal-plans/{id}/    — Update.
    DELETE /api/meal-plans/{id}/    — Delete.
    POST   /api/meal-plans/{id}/favorite/ — Toggle favourite.
    GET    /api/meal-plans/{id}/grocery/  — Grocery list for this plan.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user).prefetch_related('meals__foods', 'favorited_by')

    def get_serializer_class(self):
        if self.action == 'list':
            return MealPlanListSerializer
        return MealPlanSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        """Toggle favourite status for a meal plan."""
        plan = self.get_object()
        fav, created = FavoriteMeal.objects.get_or_create(user=request.user, meal_plan=plan)
        if not created:
            fav.delete()
            return Response({'favorited': False, 'message': 'Removed from favourites.'})
        return Response({'favorited': True, 'message': 'Added to favourites.'})

    @action(detail=True, methods=['get'])
    def grocery(self, request, pk=None):
        """Return grocery list for a meal plan."""
        plan = self.get_object()
        items = plan.grocery_items.all()
        serializer = GroceryItemSerializer(items, many=True)
        return Response(serializer.data)


class FavoriteMealListView(generics.ListAPIView):
    """GET /api/favorites/ — List all user's favourite meal plans."""
    serializer_class = FavoriteMealSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteMeal.objects.filter(user=self.request.user).select_related('meal_plan')


class GroceryItemUpdateView(generics.UpdateAPIView):
    """PATCH /api/grocery/{id}/ — Mark grocery item as purchased."""
    serializer_class = GroceryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GroceryItem.objects.filter(meal_plan__user=self.request.user)
