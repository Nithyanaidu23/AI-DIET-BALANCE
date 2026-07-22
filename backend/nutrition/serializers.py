from rest_framework import serializers
from .models import Food


class FoodSerializer(serializers.ModelSerializer):
    """Full food serializer including nutrition per serving."""
    nutrition_per_serving = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = '__all__'

    def get_nutrition_per_serving(self, obj):
        return obj.nutrition_per_serving()


class FoodMiniSerializer(serializers.ModelSerializer):
    """Lightweight serializer for embedding foods in meal responses."""
    class Meta:
        model = Food
        fields = ('id', 'name', 'category', 'calories', 'protein_g', 'carbs_g', 'fat_g', 'serving_size_g', 'serving_description')
