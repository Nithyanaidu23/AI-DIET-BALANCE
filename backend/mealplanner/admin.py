from django.contrib import admin
from .models import MealPlan, Meal, FavoriteMeal, GroceryItem


class MealInline(admin.TabularInline):
    model = Meal
    extra = 0
    fields = ('day_number', 'meal_type', 'name', 'calories', 'protein_g', 'carbs_g', 'fat_g')


class GroceryInline(admin.TabularInline):
    model = GroceryItem
    extra = 0


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'start_date', 'end_date', 'target_calories', 'ai_generated', 'created_at')
    list_filter = ('ai_generated',)
    search_fields = ('user__email', 'title')
    inlines = [MealInline, GroceryInline]


@admin.register(FavoriteMeal)
class FavoriteMealAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_plan', 'saved_at')
