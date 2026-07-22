from django.contrib import admin
from .models import Food


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'calories', 'protein_g', 'carbs_g', 'fat_g', 'is_vegetarian', 'is_vegan')
    list_filter = ('category', 'is_vegetarian', 'is_vegan', 'is_gluten_free')
    search_fields = ('name', 'name_local')
    ordering = ('category', 'name')
    list_per_page = 50
