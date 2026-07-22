"""
Thread-safe Export Engine for automatic CSV and JSON data synchronization.
Maintains files in backend/exports/ folder.
"""
import csv
import json
import logging
import os
import threading
import zipfile
from io import BytesIO
from pathlib import Path
from typing import List, Dict, Any

from django.conf import settings

logger = logging.getLogger('activity_logs')

EXPORT_DIR = getattr(settings, 'EXPORTS_DIR', Path(settings.BASE_DIR) / 'exports')
_export_lock = threading.Lock()


def ensure_export_dir():
    """Ensure the exports/ directory exists."""
    os.makedirs(EXPORT_DIR, exist_ok=True)


class ExportEngine:
    """
    Service for writing DB records to dual CSV and JSON files.
    """

    @staticmethod
    def _write_csv(file_path: Path, fieldnames: List[str], rows: List[Dict[str, Any]]):
        """Write a complete set of rows to CSV with headers (thread-safe, Windows/OneDrive compatible)."""
        ensure_export_dir()
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
        except Exception as exc:
            logger.error(f"Error writing CSV file {file_path}: {exc}")

    @staticmethod
    def _write_json(file_path: Path, rows: List[Dict[str, Any]]):
        """Write rows to JSON array (thread-safe, Windows/OneDrive compatible)."""
        ensure_export_dir()
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(rows, f, indent=2, default=str, ensure_ascii=False)
        except Exception as exc:
            logger.error(f"Error writing JSON file {file_path}: {exc}")

    @staticmethod
    def _write_excel(file_path: Path, fieldnames: List[str], rows: List[Dict[str, Any]]):
        """Write rows to Excel .xlsx spreadsheet using pandas/openpyxl if installed."""
        ensure_export_dir()
        try:
            import pandas as pd
            df = pd.DataFrame(rows, columns=fieldnames)
            df.to_excel(file_path, index=False, engine='openpyxl')
        except (ImportError, ModuleNotFoundError):
            pass
        except Exception as exc:
            logger.error(f"Error writing Excel file {file_path}: {exc}")


    @classmethod
    def sync_entity(cls, entity_name: str, fieldnames: List[str], rows: List[Dict[str, Any]]):
        """
        Thread-safe synchronization of entity records to exports/{entity_name}.csv, .json, and .xlsx
        """
        with _export_lock:
            ensure_export_dir()
            csv_path = EXPORT_DIR / f"{entity_name}.csv"
            json_path = EXPORT_DIR / f"{entity_name}.json"
            excel_path = EXPORT_DIR / f"{entity_name}.xlsx"

            cls._write_csv(csv_path, fieldnames, rows)
            cls._write_json(json_path, rows)
            cls._write_excel(excel_path, fieldnames, rows)


def export_all():
    """
    Export all models across the application into exports/*.csv, exports/*.json, and exports/*.xlsx files.
    """
    from django.contrib.auth import get_user_model
    from users.models import UserProfile, Notification, Feedback
    from nutrition.models import Food
    from mealplanner.models import MealPlan
    from health.models import BMIRecord, WaterTracker, ExerciseLog
    from activity_logs.models import LoginHistory, ActivityLog, AnalyticsEvent
    from accounts.models import Subscription, Payment

    User = get_user_model()

    # 1. Users
    user_fields = ['id', 'first_name', 'last_name', 'email', 'role', 'is_active', 'is_staff', 'date_joined', 'last_login', 'google_id']
    users_data = []
    for u in User.objects.all().order_by('id'):
        users_data.append({
            'id': u.id,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'role': u.role,
            'is_active': u.is_active,
            'is_staff': u.is_staff,
            'date_joined': u.date_joined.isoformat() if u.date_joined else '',
            'last_login': u.last_login.isoformat() if u.last_login else '',
            'google_id': u.google_id or '',
        })
    ExportEngine.sync_entity('users', user_fields, users_data)

    # 2. Subscriptions
    sub_fields = ['id', 'user_id', 'user_email', 'plan', 'status', 'stripe_customer_id', 'stripe_subscription_id', 'current_period_start', 'current_period_end', 'created_at']
    sub_data = []
    for s in Subscription.objects.select_related('user').all().order_by('id'):
        sub_data.append({
            'id': s.id,
            'user_id': s.user_id,
            'user_email': s.user.email if s.user else '',
            'plan': s.plan,
            'status': s.status,
            'stripe_customer_id': s.stripe_customer_id or '',
            'stripe_subscription_id': s.stripe_subscription_id or '',
            'current_period_start': s.current_period_start.isoformat() if s.current_period_start else '',
            'current_period_end': s.current_period_end.isoformat() if s.current_period_end else '',
            'created_at': s.created_at.isoformat() if s.created_at else '',
        })
    ExportEngine.sync_entity('subscriptions', sub_fields, sub_data)

    # 3. Payments
    pay_fields = ['id', 'user_id', 'user_email', 'amount', 'currency', 'stripe_charge_id', 'status', 'created_at']
    pay_data = []
    for pm in Payment.objects.select_related('user').all().order_by('id'):
        pay_data.append({
            'id': pm.id,
            'user_id': pm.user_id,
            'user_email': pm.user.email if pm.user else '',
            'amount': str(pm.amount),
            'currency': pm.currency,
            'stripe_charge_id': pm.stripe_charge_id or '',
            'status': pm.status,
            'created_at': pm.created_at.isoformat() if pm.created_at else '',
        })
    ExportEngine.sync_entity('payments', pay_fields, pay_data)

    # 4. Login History
    lh_fields = ['id', 'user_id', 'user_name', 'user_email', 'login_time', 'logout_time', 'ip_address', 'browser_name', 'os_name', 'device_type', 'session_id', 'status', 'failed_login_count']
    lh_data = []
    for lh in LoginHistory.objects.all().order_by('id'):
        lh_data.append({
            'id': lh.id,
            'user_id': lh.user_id or '',
            'user_name': lh.user_name or '',
            'user_email': lh.user_email,
            'login_time': lh.login_time.isoformat() if lh.login_time else '',
            'logout_time': lh.logout_time.isoformat() if lh.logout_time else '',
            'ip_address': lh.ip_address or '',
            'browser_name': lh.browser_name,
            'os_name': lh.os_name,
            'device_type': lh.device_type,
            'session_id': lh.session_id,
            'status': lh.status,
            'failed_login_count': lh.failed_login_count,
        })
    ExportEngine.sync_entity('login_history', lh_fields, lh_data)

    # 5. Profiles
    profile_fields = ['id', 'user_id', 'user_email', 'age', 'gender', 'height_cm', 'weight_kg', 'activity_level', 'fitness_goal', 'food_preference', 'allergies', 'medical_conditions', 'country', 'cuisine_preference', 'budget_per_day_usd', 'workout_time', 'updated_at']
    profiles_data = []
    for p in UserProfile.objects.select_related('user').all().order_by('id'):
        profiles_data.append({
            'id': p.id,
            'user_id': p.user_id,
            'user_email': p.user.email if p.user else '',
            'age': p.age or '',
            'gender': p.gender or '',
            'height_cm': str(p.height_cm) if p.height_cm else '',
            'weight_kg': str(p.weight_kg) if p.weight_kg else '',
            'activity_level': p.activity_level or '',
            'fitness_goal': p.fitness_goal or '',
            'food_preference': p.food_preference or '',
            'allergies': p.allergies or '',
            'medical_conditions': p.medical_conditions or '',
            'country': p.country or '',
            'cuisine_preference': p.cuisine_preference or '',
            'budget_per_day_usd': str(p.budget_per_day_usd) if p.budget_per_day_usd else '',
            'workout_time': p.workout_time or '',
            'updated_at': p.updated_at.isoformat() if p.updated_at else '',
        })
    ExportEngine.sync_entity('profiles', profile_fields, profiles_data)

    # 6. Meal Plans
    mp_fields = ['id', 'user_id', 'user_email', 'title', 'start_date', 'end_date', 'target_calories', 'target_protein_g', 'target_carbs_g', 'target_fat_g', 'ai_generated', 'created_at', 'meals_count', 'grocery_items_count']
    mp_data = []
    for mp in MealPlan.objects.select_related('user').prefetch_related('meals', 'grocery_items').all().order_by('id'):
        mp_data.append({
            'id': mp.id,
            'user_id': mp.user_id,
            'user_email': mp.user.email if mp.user else '',
            'title': mp.title,
            'start_date': mp.start_date.isoformat() if mp.start_date else '',
            'end_date': mp.end_date.isoformat() if mp.end_date else '',
            'target_calories': mp.target_calories,
            'target_protein_g': mp.target_protein_g,
            'target_carbs_g': mp.target_carbs_g,
            'target_fat_g': mp.target_fat_g,
            'ai_generated': mp.ai_generated,
            'created_at': mp.created_at.isoformat() if mp.created_at else '',
            'meals_count': mp.meals.count(),
            'grocery_items_count': mp.grocery_items.count(),
        })
    ExportEngine.sync_entity('meal_plans', mp_fields, mp_data)

    # 7. Foods
    food_fields = ['id', 'name', 'name_local', 'category', 'calories', 'protein_g', 'carbs_g', 'fat_g', 'fiber_g', 'serving_size_g', 'serving_description', 'is_vegetarian', 'is_vegan', 'is_gluten_free']
    foods_data = []
    for f in Food.objects.all().order_by('id'):
        foods_data.append({
            'id': f.id,
            'name': f.name,
            'name_local': f.name_local or '',
            'category': f.category,
            'calories': str(f.calories),
            'protein_g': str(f.protein_g),
            'carbs_g': str(f.carbs_g),
            'fat_g': str(f.fat_g),
            'fiber_g': str(f.fiber_g),
            'serving_size_g': str(f.serving_size_g),
            'serving_description': f.serving_description or '',
            'is_vegetarian': f.is_vegetarian,
            'is_vegan': f.is_vegan,
            'is_gluten_free': f.is_gluten_free,
        })
    ExportEngine.sync_entity('foods', food_fields, foods_data)

    # 8. BMI History
    bmi_fields = ['id', 'user_id', 'user_email', 'weight_kg', 'height_cm', 'bmi', 'bmi_category', 'body_fat_percent', 'ideal_weight_kg', 'goal_calories', 'recorded_at']
    bmi_data = []
    for b in BMIRecord.objects.select_related('user').all().order_by('id'):
        bmi_data.append({
            'id': b.id,
            'user_id': b.user_id,
            'user_email': b.user.email if b.user else '',
            'weight_kg': str(b.weight_kg),
            'height_cm': str(b.height_cm),
            'bmi': str(b.bmi),
            'bmi_category': b.bmi_category,
            'body_fat_percent': str(b.body_fat_percent) if b.body_fat_percent else '',
            'ideal_weight_kg': str(b.ideal_weight_kg) if b.ideal_weight_kg else '',
            'goal_calories': b.goal_calories or '',
            'recorded_at': b.recorded_at.isoformat() if b.recorded_at else '',
        })
    ExportEngine.sync_entity('bmi_history', bmi_fields, bmi_data)

    # 9. Water Tracker
    water_fields = ['id', 'user_id', 'user_email', 'date', 'amount_ml', 'target_ml', 'percent_complete']
    water_data = []
    for w in WaterTracker.objects.select_related('user').all().order_by('id'):
        water_data.append({
            'id': w.id,
            'user_id': w.user_id,
            'user_email': w.user.email if w.user else '',
            'date': w.date.isoformat() if w.date else '',
            'amount_ml': w.amount_ml,
            'target_ml': w.target_ml,
            'percent_complete': w.percent_complete,
        })
    ExportEngine.sync_entity('water_tracker', water_fields, water_data)

    # 10. Exercise Logs
    ex_fields = ['id', 'user_id', 'user_email', 'exercise_name', 'duration_minutes', 'calories_burned', 'logged_at']
    ex_data = []
    for ex in ExerciseLog.objects.select_related('user').all().order_by('id'):
        ex_data.append({
            'id': ex.id,
            'user_id': ex.user_id,
            'user_email': ex.user.email if ex.user else '',
            'exercise_name': ex.exercise_name,
            'duration_minutes': ex.duration_minutes,
            'calories_burned': ex.calories_burned,
            'logged_at': ex.logged_at.isoformat() if ex.logged_at else '',
        })
    ExportEngine.sync_entity('exercise_logs', ex_fields, ex_data)

    # 11. Events
    event_fields = ['id', 'user_id', 'user_email', 'event_name', 'timestamp', 'metadata']
    ev_data = []
    for ev in AnalyticsEvent.objects.select_related('user').all().order_by('id'):
        ev_data.append({
            'id': ev.id,
            'user_id': ev.user_id or '',
            'user_email': ev.user.email if ev.user else 'Anonymous',
            'event_name': ev.event_name,
            'timestamp': ev.timestamp.isoformat() if ev.timestamp else '',
            'metadata': json.dumps(ev.metadata),
        })
    ExportEngine.sync_entity('events', event_fields, ev_data)

    # 12. Activity Logs
    act_fields = ['id', 'user_id', 'user_email', 'action', 'description', 'ip_address', 'timestamp']
    act_data = []
    for a in ActivityLog.objects.select_related('user').all().order_by('id'):
        act_data.append({
            'id': a.id,
            'user_id': a.user_id or '',
            'user_email': a.user.email if a.user else 'Anonymous',
            'action': a.action,
            'description': a.description,
            'ip_address': a.ip_address or '',
            'timestamp': a.timestamp.isoformat() if a.timestamp else '',
        })
    ExportEngine.sync_entity('activity_logs', act_fields, act_data)


def create_export_zip_buffer() -> BytesIO:
    """
    Package all files in exports/ into an in-memory ZIP archive.
    """
    export_all()  # ensure exports/ is fully up-to-date
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in EXPORT_DIR.glob('*.*'):
            if file_path.suffix in ['.csv', '.json', '.xlsx']:
                zip_file.write(file_path, arcname=file_path.name)

    zip_buffer.seek(0)
    return zip_buffer

