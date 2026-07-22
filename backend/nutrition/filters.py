import django_filters
from .models import Food, FoodCategory


class FoodFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(choices=FoodCategory.choices)
    is_vegetarian = django_filters.BooleanFilter()
    is_vegan = django_filters.BooleanFilter()
    is_gluten_free = django_filters.BooleanFilter()
    min_protein = django_filters.NumberFilter(field_name='protein_g', lookup_expr='gte')
    max_calories = django_filters.NumberFilter(field_name='calories', lookup_expr='lte')

    class Meta:
        model = Food
        fields = ['category', 'is_vegetarian', 'is_vegan', 'is_gluten_free']
