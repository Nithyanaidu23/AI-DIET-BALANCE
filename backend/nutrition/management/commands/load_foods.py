"""
Management command: python manage.py load_foods
Seeds the nutrition database with 60+ common foods.
Safe to run multiple times — uses get_or_create.
"""
from django.core.management.base import BaseCommand
from nutrition.models import Food, FoodCategory

FOODS = [
    # Grains
    {'name': 'White Rice', 'category': FoodCategory.GRAINS, 'calories': 130, 'protein_g': 2.7, 'carbs_g': 28.2, 'fat_g': 0.3, 'fiber_g': 0.4, 'serving_size_g': 180, 'serving_description': '1 cup cooked', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Brown Rice', 'category': FoodCategory.GRAINS, 'calories': 123, 'protein_g': 2.7, 'carbs_g': 25.6, 'fat_g': 1.0, 'fiber_g': 1.6, 'serving_size_g': 180, 'serving_description': '1 cup cooked', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Oats', 'category': FoodCategory.GRAINS, 'calories': 389, 'protein_g': 16.9, 'carbs_g': 66.3, 'fat_g': 6.9, 'fiber_g': 10.6, 'serving_size_g': 80, 'serving_description': '1 cup dry', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Whole Wheat Bread', 'category': FoodCategory.GRAINS, 'calories': 247, 'protein_g': 13.0, 'carbs_g': 41.0, 'fat_g': 4.2, 'fiber_g': 6.0, 'serving_size_g': 30, 'serving_description': '1 slice'},
    {'name': 'Quinoa', 'category': FoodCategory.GRAINS, 'calories': 120, 'protein_g': 4.4, 'carbs_g': 21.3, 'fat_g': 1.9, 'fiber_g': 2.8, 'serving_size_g': 185, 'serving_description': '1 cup cooked', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Chapati / Roti', 'category': FoodCategory.GRAINS, 'calories': 297, 'protein_g': 9.0, 'carbs_g': 55.0, 'fat_g': 4.0, 'fiber_g': 4.5, 'serving_size_g': 40, 'serving_description': '1 medium roti', 'is_vegetarian': True, 'is_vegan': True},

    # Protein sources
    {'name': 'Chicken Breast', 'category': FoodCategory.PROTEIN, 'calories': 165, 'protein_g': 31.0, 'carbs_g': 0.0, 'fat_g': 3.6, 'fiber_g': 0.0, 'serving_size_g': 100, 'serving_description': '100g cooked', 'is_gluten_free': True},
    {'name': 'Chicken Thigh', 'category': FoodCategory.PROTEIN, 'calories': 209, 'protein_g': 26.0, 'carbs_g': 0.0, 'fat_g': 11.0, 'fiber_g': 0.0, 'serving_size_g': 100, 'serving_description': '100g cooked', 'is_gluten_free': True},
    {'name': 'Salmon', 'category': FoodCategory.PROTEIN, 'calories': 208, 'protein_g': 20.0, 'carbs_g': 0.0, 'fat_g': 13.4, 'fiber_g': 0.0, 'serving_size_g': 100, 'serving_description': '100g cooked', 'is_gluten_free': True},
    {'name': 'Tuna (canned)', 'category': FoodCategory.PROTEIN, 'calories': 116, 'protein_g': 25.5, 'carbs_g': 0.0, 'fat_g': 0.8, 'fiber_g': 0.0, 'serving_size_g': 85, 'serving_description': '1 can drained', 'is_gluten_free': True},
    {'name': 'Tilapia', 'category': FoodCategory.PROTEIN, 'calories': 129, 'protein_g': 26.0, 'carbs_g': 0.0, 'fat_g': 2.7, 'fiber_g': 0.0, 'serving_size_g': 100, 'serving_description': '100g cooked', 'is_gluten_free': True},
    {'name': 'Eggs', 'category': FoodCategory.DAIRY, 'calories': 155, 'protein_g': 13.0, 'carbs_g': 1.1, 'fat_g': 11.0, 'fiber_g': 0.0, 'serving_size_g': 50, 'serving_description': '1 large egg', 'is_vegetarian': True, 'is_gluten_free': True},
    {'name': 'Egg Whites', 'category': FoodCategory.DAIRY, 'calories': 52, 'protein_g': 11.0, 'carbs_g': 0.7, 'fat_g': 0.2, 'fiber_g': 0.0, 'serving_size_g': 100, 'serving_description': '100g / ~3 egg whites', 'is_vegetarian': True, 'is_gluten_free': True},
    {'name': 'Paneer', 'category': FoodCategory.DAIRY, 'calories': 265, 'protein_g': 18.3, 'carbs_g': 1.2, 'fat_g': 20.8, 'fiber_g': 0.0, 'serving_size_g': 100, 'serving_description': '100g', 'is_vegetarian': True, 'is_gluten_free': True},
    {'name': 'Tofu (firm)', 'category': FoodCategory.PROTEIN, 'calories': 76, 'protein_g': 8.1, 'carbs_g': 1.9, 'fat_g': 4.2, 'fiber_g': 0.3, 'serving_size_g': 100, 'serving_description': '100g', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},

    # Dairy
    {'name': 'Whole Milk', 'category': FoodCategory.DAIRY, 'calories': 61, 'protein_g': 3.2, 'carbs_g': 4.8, 'fat_g': 3.3, 'fiber_g': 0.0, 'serving_size_g': 240, 'serving_description': '1 cup', 'is_vegetarian': True, 'is_gluten_free': True},
    {'name': 'Greek Yogurt', 'category': FoodCategory.DAIRY, 'calories': 59, 'protein_g': 10.0, 'carbs_g': 3.6, 'fat_g': 0.4, 'fiber_g': 0.0, 'serving_size_g': 170, 'serving_description': '1 container', 'is_vegetarian': True, 'is_gluten_free': True},
    {'name': 'Cheddar Cheese', 'category': FoodCategory.DAIRY, 'calories': 402, 'protein_g': 25.0, 'carbs_g': 1.3, 'fat_g': 33.0, 'fiber_g': 0.0, 'serving_size_g': 28, 'serving_description': '1 oz slice', 'is_vegetarian': True, 'is_gluten_free': True},
    {'name': 'Cottage Cheese', 'category': FoodCategory.DAIRY, 'calories': 98, 'protein_g': 11.1, 'carbs_g': 3.4, 'fat_g': 4.3, 'fiber_g': 0.0, 'serving_size_g': 113, 'serving_description': '½ cup', 'is_vegetarian': True, 'is_gluten_free': True},

    # Legumes
    {'name': 'Lentils (Masoor Dal)', 'category': FoodCategory.LEGUMES, 'calories': 116, 'protein_g': 9.0, 'carbs_g': 20.0, 'fat_g': 0.4, 'fiber_g': 7.9, 'serving_size_g': 198, 'serving_description': '1 cup cooked', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Chickpeas (Chana)', 'category': FoodCategory.LEGUMES, 'calories': 164, 'protein_g': 8.9, 'carbs_g': 27.4, 'fat_g': 2.6, 'fiber_g': 7.6, 'serving_size_g': 164, 'serving_description': '1 cup cooked', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Black Beans', 'category': FoodCategory.LEGUMES, 'calories': 132, 'protein_g': 8.9, 'carbs_g': 23.7, 'fat_g': 0.5, 'fiber_g': 8.7, 'serving_size_g': 172, 'serving_description': '1 cup cooked', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Kidney Beans (Rajma)', 'category': FoodCategory.LEGUMES, 'calories': 127, 'protein_g': 8.7, 'carbs_g': 22.8, 'fat_g': 0.5, 'fiber_g': 7.4, 'serving_size_g': 177, 'serving_description': '1 cup cooked', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Moong Dal', 'category': FoodCategory.LEGUMES, 'calories': 105, 'protein_g': 7.0, 'carbs_g': 19.0, 'fat_g': 0.4, 'fiber_g': 5.0, 'serving_size_g': 202, 'serving_description': '1 cup cooked', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},

    # Vegetables
    {'name': 'Broccoli', 'category': FoodCategory.VEGETABLES, 'calories': 34, 'protein_g': 2.8, 'carbs_g': 6.6, 'fat_g': 0.4, 'fiber_g': 2.6, 'serving_size_g': 91, 'serving_description': '1 cup chopped', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Spinach', 'category': FoodCategory.VEGETABLES, 'calories': 23, 'protein_g': 2.9, 'carbs_g': 3.6, 'fat_g': 0.4, 'fiber_g': 2.2, 'serving_size_g': 30, 'serving_description': '1 cup raw', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Sweet Potato', 'category': FoodCategory.VEGETABLES, 'calories': 86, 'protein_g': 1.6, 'carbs_g': 20.1, 'fat_g': 0.1, 'fiber_g': 3.0, 'serving_size_g': 130, 'serving_description': '1 medium', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Carrot', 'category': FoodCategory.VEGETABLES, 'calories': 41, 'protein_g': 0.9, 'carbs_g': 9.6, 'fat_g': 0.2, 'fiber_g': 2.8, 'serving_size_g': 61, 'serving_description': '1 medium', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Tomato', 'category': FoodCategory.VEGETABLES, 'calories': 18, 'protein_g': 0.9, 'carbs_g': 3.9, 'fat_g': 0.2, 'fiber_g': 1.2, 'serving_size_g': 123, 'serving_description': '1 medium', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Cucumber', 'category': FoodCategory.VEGETABLES, 'calories': 15, 'protein_g': 0.7, 'carbs_g': 3.6, 'fat_g': 0.1, 'fiber_g': 0.5, 'serving_size_g': 119, 'serving_description': '1 cup sliced', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Cauliflower', 'category': FoodCategory.VEGETABLES, 'calories': 25, 'protein_g': 1.9, 'carbs_g': 5.0, 'fat_g': 0.3, 'fiber_g': 2.0, 'serving_size_g': 107, 'serving_description': '1 cup', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Capsicum (Bell Pepper)', 'category': FoodCategory.VEGETABLES, 'calories': 31, 'protein_g': 1.0, 'carbs_g': 6.0, 'fat_g': 0.3, 'fiber_g': 2.1, 'serving_size_g': 119, 'serving_description': '1 medium', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},

    # Fruits
    {'name': 'Banana', 'category': FoodCategory.FRUITS, 'calories': 89, 'protein_g': 1.1, 'carbs_g': 22.8, 'fat_g': 0.3, 'fiber_g': 2.6, 'serving_size_g': 118, 'serving_description': '1 medium', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Apple', 'category': FoodCategory.FRUITS, 'calories': 52, 'protein_g': 0.3, 'carbs_g': 13.8, 'fat_g': 0.2, 'fiber_g': 2.4, 'serving_size_g': 182, 'serving_description': '1 medium', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Orange', 'category': FoodCategory.FRUITS, 'calories': 47, 'protein_g': 0.9, 'carbs_g': 11.8, 'fat_g': 0.1, 'fiber_g': 2.4, 'serving_size_g': 131, 'serving_description': '1 medium', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Mango', 'category': FoodCategory.FRUITS, 'calories': 60, 'protein_g': 0.8, 'carbs_g': 15.0, 'fat_g': 0.4, 'fiber_g': 1.6, 'serving_size_g': 165, 'serving_description': '1 cup sliced', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Blueberries', 'category': FoodCategory.FRUITS, 'calories': 57, 'protein_g': 0.7, 'carbs_g': 14.5, 'fat_g': 0.3, 'fiber_g': 2.4, 'serving_size_g': 148, 'serving_description': '1 cup', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},

    # Nuts & Seeds
    {'name': 'Almonds', 'category': FoodCategory.NUTS_SEEDS, 'calories': 579, 'protein_g': 21.2, 'carbs_g': 21.6, 'fat_g': 49.9, 'fiber_g': 12.5, 'serving_size_g': 28, 'serving_description': '1 oz (~23 almonds)', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Walnuts', 'category': FoodCategory.NUTS_SEEDS, 'calories': 654, 'protein_g': 15.2, 'carbs_g': 13.7, 'fat_g': 65.2, 'fiber_g': 6.7, 'serving_size_g': 28, 'serving_description': '1 oz (~14 halves)', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Chia Seeds', 'category': FoodCategory.NUTS_SEEDS, 'calories': 486, 'protein_g': 16.5, 'carbs_g': 42.1, 'fat_g': 30.7, 'fiber_g': 34.4, 'serving_size_g': 28, 'serving_description': '2 tablespoons', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Peanut Butter', 'category': FoodCategory.NUTS_SEEDS, 'calories': 588, 'protein_g': 25.1, 'carbs_g': 20.0, 'fat_g': 50.4, 'fiber_g': 6.0, 'serving_size_g': 32, 'serving_description': '2 tablespoons', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Flax Seeds', 'category': FoodCategory.NUTS_SEEDS, 'calories': 534, 'protein_g': 18.3, 'carbs_g': 28.9, 'fat_g': 42.2, 'fiber_g': 27.3, 'serving_size_g': 14, 'serving_description': '1 tablespoon', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},

    # Fats & Oils
    {'name': 'Olive Oil', 'category': FoodCategory.FATS_OILS, 'calories': 884, 'protein_g': 0.0, 'carbs_g': 0.0, 'fat_g': 100.0, 'fiber_g': 0.0, 'serving_size_g': 14, 'serving_description': '1 tablespoon', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Coconut Oil', 'category': FoodCategory.FATS_OILS, 'calories': 862, 'protein_g': 0.0, 'carbs_g': 0.0, 'fat_g': 100.0, 'fiber_g': 0.0, 'serving_size_g': 14, 'serving_description': '1 tablespoon', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Avocado', 'category': FoodCategory.FATS_OILS, 'calories': 160, 'protein_g': 2.0, 'carbs_g': 8.5, 'fat_g': 14.7, 'fiber_g': 6.7, 'serving_size_g': 150, 'serving_description': '1 medium', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},

    # Beverages
    {'name': 'Whey Protein (scoop)', 'category': FoodCategory.BEVERAGES, 'calories': 120, 'protein_g': 24.0, 'carbs_g': 3.0, 'fat_g': 2.0, 'fiber_g': 0.0, 'serving_size_g': 30, 'serving_description': '1 scoop', 'is_gluten_free': True},
    {'name': 'Black Coffee', 'category': FoodCategory.BEVERAGES, 'calories': 2, 'protein_g': 0.3, 'carbs_g': 0.0, 'fat_g': 0.0, 'fiber_g': 0.0, 'serving_size_g': 240, 'serving_description': '1 cup', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
    {'name': 'Green Tea', 'category': FoodCategory.BEVERAGES, 'calories': 2, 'protein_g': 0.2, 'carbs_g': 0.5, 'fat_g': 0.0, 'fiber_g': 0.0, 'serving_size_g': 240, 'serving_description': '1 cup brewed', 'is_vegetarian': True, 'is_vegan': True, 'is_gluten_free': True},
]


class Command(BaseCommand):
    help = 'Seed the nutrition database with common foods.'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for food_data in FOODS:
            name = food_data.pop('name')
            obj, created = Food.objects.update_or_create(
                name=name,
                defaults=food_data,
            )
            food_data['name'] = name  # restore for any retry

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Done! Created {created_count} new foods, updated {updated_count} existing.'
            )
        )
