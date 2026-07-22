"""
Unit tests for Automatic Export Engine, Audit Logs, and Signals.
Run with: python manage.py test activity_logs.tests
"""
import json
import os
from pathlib import Path
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import LoginHistory, ActivityLog, ActionType
from .exporter import export_all, create_export_zip_buffer, EXPORT_DIR
from users.models import UserProfile
from health.models import BMIRecord, WaterTracker

User = get_user_model()


class ExportEngineTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test_audit@example.com',
            password='Password123!',
            first_name='Audit',
            last_name='Tester'
        )

    def test_export_all_creates_files(self):
        export_all()

        expected_files = [
            'users.csv', 'users.json',
            'login_history.csv', 'login_history.json',
            'profiles.csv', 'profiles.json',
            'meal_plans.csv', 'meal_plans.json',
            'foods.csv', 'foods.json',
            'bmi_history.csv', 'bmi_history.json',
            'water_tracker.csv', 'water_tracker.json',
            'activity_logs.csv', 'activity_logs.json',
        ]

        for fname in expected_files:
            fpath = EXPORT_DIR / fname
            self.assertTrue(fpath.exists(), f"Expected export file {fname} does not exist.")
            self.assertGreaterEqual(fpath.stat().st_size, 0)

        # Check users.json contains our user
        users_json_path = EXPORT_DIR / 'users.json'
        with open(users_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            emails = [u['email'] for u in data]
            self.assertIn('test_audit@example.com', emails)

    def test_zip_export_buffer(self):
        zip_buf = create_export_zip_buffer()
        self.assertGreater(len(zip_buf.getvalue()), 0)

    def test_activity_logging(self):
        ActivityLog.objects.create(
            user=self.user,
            action=ActionType.BMI_CALCULATED,
            description="Calculated BMI 22.5",
            ip_address="127.0.0.1"
        )
        export_all()

        act_json_path = EXPORT_DIR / 'activity_logs.json'
        with open(act_json_path, 'r', encoding='utf-8') as f:
            logs = json.load(f)
            actions = [l['action'] for l in logs]
            self.assertIn('BMI_CALCULATED', actions)
