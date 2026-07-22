"""Meal planning models — MealPlan, Meal, MealHistory, FavoriteMeal, GroceryItem."""
from django.conf import settings
from django.db import models
from nutrition.models import Food


class MealType(models.TextChoices):
    BREAKFAST = 'breakfast', 'Breakfast'
    LUNCH = 'lunch', 'Lunch'
    DINNER = 'dinner', 'Dinner'
    SNACK = 'snack', 'Snack'
    PRE_WORKOUT = 'pre_workout', 'Pre-Workout'
    POST_WORKOUT = 'post_workout', 'Post-Workout'


class MealPlan(models.Model):
    """A complete AI-generated or user-created diet plan for a specific date range."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meal_plans'
    )
    title = models.CharField(max_length=200, blank=True, default='My Meal Plan')
    start_date = models.DateField()
    end_date = models.DateField()

    # Daily targets
    target_calories = models.IntegerField()
    target_protein_g = models.IntegerField(default=0)
    target_carbs_g = models.IntegerField(default=0)
    target_fat_g = models.IntegerField(default=0)
    target_water_ml = models.IntegerField(default=2500)

    # Metadata from AI generation
    ai_generated = models.BooleanField(default=False)
    ai_prompt_summary = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Meal Plan'
        verbose_name_plural = 'Meal Plans'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} — {self.title} ({self.start_date})'


class Meal(models.Model):
    """A single meal within a meal plan (e.g., Monday Breakfast)."""
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='meals')
    meal_type = models.CharField(max_length=20, choices=MealType.choices)
    day_number = models.PositiveSmallIntegerField(default=1, help_text='Day 1–7 within the plan')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Macros for this meal (denormalised for speed)
    calories = models.IntegerField()
    protein_g = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    carbs_g = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    fat_g = models.DecimalField(max_digits=6, decimal_places=1, default=0)

    # Linked foods (optional)
    foods = models.ManyToManyField(Food, blank=True, related_name='meals')

    # Recipe / instructions
    recipe_steps = models.TextField(blank=True)
    prep_time_minutes = models.PositiveSmallIntegerField(null=True, blank=True)
    cook_time_minutes = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Meal'
        verbose_name_plural = 'Meals'
        ordering = ['day_number', 'meal_type']

    def __str__(self):
        return f'Day {self.day_number} {self.meal_type}: {self.name}'


class FavoriteMeal(models.Model):
    """User-saved favourite meal plans."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites'
    )
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='favorited_by')
    note = models.CharField(max_length=300, blank=True)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'meal_plan')
        verbose_name = 'Favourite Meal'
        verbose_name_plural = 'Favourite Meals'

    def __str__(self):
        return f'{self.user.email} ❤ {self.meal_plan.title}'


class GroceryItem(models.Model):
    """Auto-generated grocery list item linked to a meal plan."""
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='grocery_items')
    name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, default=1)
    unit = models.CharField(max_length=50, blank=True, help_text='e.g., grams, cups, pieces')
    category = models.CharField(max_length=100, blank=True)
    purchased = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Grocery Item'
        verbose_name_plural = 'Grocery Items'
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.quantity}{self.unit} {self.name}'
