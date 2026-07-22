"""Unit tests for user profile API."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserProfile

User = get_user_model()


class UserProfileAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='profile@example.com', password='Password123!')
        self.client.force_authenticate(user=self.user)
        self.profile_url = '/api/profile/'

    def test_get_profile_auto_creates(self):
        res = self.client.get(self.profile_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

    def test_update_profile(self):
        payload = {
            'age': 28,
            'height_cm': 175.0,
            'weight_kg': 72.5,
            'fitness_goal': 'lose_fat',
            'activity_level': 'moderate',
        }
        res = self.client.put(self.profile_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.age, 28)
        self.assertEqual(float(profile.weight_kg), 72.5)
