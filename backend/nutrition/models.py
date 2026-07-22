"""Food model for the nutrition database."""
from django.db import models


class FoodCategory(models.TextChoices):
    GRAINS = 'grains', 'Grains & Cereals'
    PROTEIN = 'protein', 'Protein Sources'
    DAIRY = 'dairy', 'Dairy & Eggs'
    VEGETABLES = 'vegetables', 'Vegetables'
    FRUITS = 'fruits', 'Fruits'
    LEGUMES = 'legumes', 'Legumes & Pulses'
    NUTS_SEEDS = 'nuts_seeds', 'Nuts & Seeds'
    FATS_OILS = 'fats_oils', 'Fats & Oils'
    BEVERAGES = 'beverages', 'Beverages'
    SNACKS = 'snacks', 'Snacks & Others'


class Food(models.Model):
    """
    Nutrition database entry.
    All macro values are per 100g unless serving_size_g is specified differently.
    """
    name = models.CharField(max_length=200, db_index=True)
    name_local = models.CharField(max_length=200, blank=True, help_text='Local/regional name')
    category = models.CharField(max_length=20, choices=FoodCategory.choices, default=FoodCategory.PROTEIN)

    # Per 100g values
    calories = models.DecimalField(max_digits=7, decimal_places=2)
    protein_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    carbs_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fat_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fiber_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    sugar_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    sodium_mg = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # Serving
    serving_size_g = models.DecimalField(
        max_digits=6, decimal_places=1, default=100,
        help_text='Default serving size in grams'
    )
    serving_description = models.CharField(max_length=100, blank=True, help_text='e.g., 1 cup, 1 medium')

    # Flags
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)

    # Image
    image = models.ImageField(upload_to='foods/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Foods'
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f'{self.name} ({self.category})'

    def nutrition_per_serving(self):
        """Return nutrition values scaled to the default serving size."""
        factor = float(self.serving_size_g) / 100
        return {
            'calories': round(float(self.calories) * factor, 1),
            'protein_g': round(float(self.protein_g) * factor, 1),
            'carbs_g': round(float(self.carbs_g) * factor, 1),
            'fat_g': round(float(self.fat_g) * factor, 1),
            'fiber_g': round(float(self.fiber_g) * factor, 1),
        }
