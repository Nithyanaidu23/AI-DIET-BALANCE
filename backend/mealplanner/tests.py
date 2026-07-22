"""Unit tests for Meal Plan CRUD and Favorites."""
from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import MealPlan, FavoriteMeal

User = get_user_model()


class MealPlannerAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='planner@example.com', password='Password123!')
        self.client.force_authenticate(user=self.user)
        self.plan = MealPlan.objects.create(
            user=self.user,
            title='Sample 7-Day Plan',
            start_date=date.today(),
            end_date=date.today(),
            target_calories=2000,
            target_protein_g=150,
            target_carbs_g=200,
            target_fat_g=65,
        )

    def test_list_meal_plans(self):
        res = self.client.get('/api/meal-plans/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_toggle_favorite(self):
        res = self.client.post(f'/api/meal-plans/{self.plan.id}/favorite/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(FavoriteMeal.objects.filter(user=self.user, meal_plan=self.plan).exists())

        # Toggle off
        res_off = self.client.post(f'/api/meal-plans/{self.plan.id}/favorite/')
        self.assertEqual(res_off.status_code, status.HTTP_200_OK)
        self.assertFalse(FavoriteMeal.objects.filter(user=self.user, meal_plan=self.plan).exists())
