"""Unit tests for Nutrition Food database API and seed command."""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Food, FoodCategory


class NutritionAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.food = Food.objects.create(
            name='Test Oats',
            category=FoodCategory.GRAINS,
            calories=389,
            protein_g=16.9,
            carbs_g=66.3,
            fat_g=6.9,
            serving_size_g=80,
            is_vegetarian=True,
            is_vegan=True,
        )

    def test_list_foods(self):
        res = self.client.get('/api/foods/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_search_foods(self):
        res = self.client.get('/api/foods/', {'search': 'Oats'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_food_detail(self):
        res = self.client.get(f'/api/foods/{self.food.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], 'Test Oats')
