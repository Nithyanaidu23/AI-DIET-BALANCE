"""Unit tests for AI Prompt Builder and Response Parser."""
# pyrefly: ignore [missing-import]
from django.test import TestCase
from .prompt_builder import build_meal_plan_prompt
from .response_parser import validate_and_parse, ValidationError


class AIEngineUnitTests(TestCase):

    def test_build_prompt_contains_user_data(self):
        user_data = {
            'age': 25,
            'gender': 'male',
            'height_cm': 175,
            'weight_kg': 70,
            'goal': 'lose_fat',
            'target_calories': 2000,
        }
        prompt = build_meal_plan_prompt(user_data, [])
        self.assertIn('2000', prompt)
        self.assertIn('fat loss', prompt)

    def test_validate_and_parse_valid_json(self):
        sample = {
            'plan_title': 'Weight Loss Plan',
            'daily_targets': {'calories': 2000, 'protein_g': 150, 'carbs_g': 200, 'fat_g': 65, 'water_ml': 2500},
            'days': [
                {
                    'day_number': 1,
                    'day_name': 'Monday',
                    'meals': [
                        {
                            'meal_type': 'breakfast',
                            'name': 'Oatmeal & Berries',
                            'description': 'Healthy oats',
                            'calories': 400,
                            'protein_g': 20,
                            'carbs_g': 60,
                            'fat_g': 10,
                        }
                    ]
                }
            ],
            'grocery_list': [{'name': 'Oats', 'quantity': 1, 'unit': 'kg', 'category': 'Grains'}]
        }
        parsed = validate_and_parse(sample)
        self.assertEqual(parsed['plan_title'], 'Weight Loss Plan')
        self.assertEqual(len(parsed['days']), 1)

    def test_validate_and_parse_invalid_json(self):
        with self.assertRaises(ValidationError):
            validate_and_parse({'invalid_key': 123})
