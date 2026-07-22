"""Unit tests for authentication APIs (register, login, me, change-password)."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AuthAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/register/'
        self.login_url = '/api/login/'
        self.me_url = '/api/me/'
        self.change_password_url = '/api/change-password/'

    def test_user_registration_success(self):
        payload = {
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        }
        res = self.client.post(self.register_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_user_registration_password_mismatch(self):
        payload = {
            'email': 'baduser@example.com',
            'first_name': 'Bad',
            'password': 'Password123!',
            'password2': 'Different123!',
        }
        res = self.client.post(self.register_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_and_jwt_issuance(self):
        User.objects.create_user(email='login@example.com', password='MyPassword123!')
        res = self.client.post(self.login_url, {'email': 'login@example.com', 'password': 'MyPassword123!'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_me_endpoint_authenticated(self):
        user = User.objects.create_user(email='me@example.com', password='MyPassword123!')
        self.client.force_authenticate(user=user)
        res = self.client.get(self.me_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], 'me@example.com')
