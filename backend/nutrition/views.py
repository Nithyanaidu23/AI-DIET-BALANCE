from rest_framework import viewsets, permissions
from .models import Food
from .serializers import FoodSerializer
from .filters import FoodFilter


class FoodViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/foods/        — List all foods (with search & filter).
    GET /api/foods/{id}/   — Retrieve a single food item.
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = FoodFilter
    search_fields = ['name', 'name_local', 'category']
    ordering_fields = ['name', 'calories', 'protein_g']
    ordering = ['category', 'name']
