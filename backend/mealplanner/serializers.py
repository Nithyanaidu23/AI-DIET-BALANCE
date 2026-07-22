"""Serializers for meal planning."""
from rest_framework import serializers
from nutrition.serializers import FoodMiniSerializer
from .models import MealPlan, Meal, FavoriteMeal, GroceryItem


class MealSerializer(serializers.ModelSerializer):
    foods = FoodMiniSerializer(many=True, read_only=True)
    food_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=__import__('nutrition.models', fromlist=['Food']).Food.objects.all(),
        source='foods', required=False
    )

    class Meta:
        model = Meal
        exclude = ('meal_plan',)


class MealPlanSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = MealPlan
        exclude = ('user',)
        read_only_fields = ('id', 'created_at', 'updated_at', 'ai_generated')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(user=request.user).exists()
        return False


class MealPlanListSerializer(serializers.ModelSerializer):
    """Lightweight list serializer — no nested meals."""
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = MealPlan
        fields = ('id', 'title', 'start_date', 'end_date', 'target_calories',
                  'target_protein_g', 'target_carbs_g', 'target_fat_g',
                  'ai_generated', 'created_at', 'is_favorited')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(user=request.user).exists()
        return False


class GroceryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroceryItem
        exclude = ('meal_plan',)


class FavoriteMealSerializer(serializers.ModelSerializer):
    meal_plan = MealPlanListSerializer(read_only=True)

    class Meta:
        model = FavoriteMeal
        fields = ('id', 'meal_plan', 'note', 'saved_at')
        read_only_fields = ('id', 'saved_at')
