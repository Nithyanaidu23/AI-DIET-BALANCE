"""
Automated ETL Data Pipeline (Database -> Extract -> Transform -> Load -> Warehouse Analytics)
Extracts raw user, diet, health, and event records, performs data transformations using Pandas,
and loads aggregated summaries into exports/analytics_warehouse_summary.json and .csv.
"""
import json
import logging
from pathlib import Path

import pandas as pd
from django.conf import settings

logger = logging.getLogger('activity_logs')

EXPORT_DIR = getattr(settings, 'EXPORTS_DIR', Path(settings.BASE_DIR) / 'exports')


def run_etl_pipeline() -> dict:
    """
    Execute full ETL pipeline:
    1. Extract records from DB (Users, MealPlans, BMIRecords, Events).
    2. Transform metrics using Pandas (averages, distributions, event counts).
    3. Load output to analytics summary files.
    """
    from django.contrib.auth import get_user_model
    from mealplanner.models import MealPlan
    from health.models import BMIRecord
    from activity_logs.models import AnalyticsEvent, ActivityLog

    User = get_user_model()

    # 1. EXTRACT
    users = list(User.objects.values('id', 'email', 'role', 'date_joined'))
    meal_plans = list(MealPlan.objects.values('id', 'user_id', 'target_calories', 'ai_generated', 'created_at'))
    bmi_records = list(BMIRecord.objects.values('id', 'user_id', 'bmi', 'weight_kg', 'recorded_at'))
    events = list(AnalyticsEvent.objects.values('id', 'user_id', 'event_name', 'timestamp'))

    # 2. TRANSFORM
    users_df = pd.DataFrame(users) if users else pd.DataFrame(columns=['id', 'role'])
    plans_df = pd.DataFrame(meal_plans) if meal_plans else pd.DataFrame(columns=['target_calories', 'ai_generated'])
    bmi_df = pd.DataFrame(bmi_records) if bmi_records else pd.DataFrame(columns=['bmi', 'weight_kg'])
    events_df = pd.DataFrame(events) if events else pd.DataFrame(columns=['event_name'])

    transformed_summary = {
        'total_registered_users': int(len(users_df)),
        'users_by_role': users_df['role'].value_counts().to_dict() if not users_df.empty else {},
        'total_meal_plans_generated': int(len(plans_df)),
        'average_target_calories': float(plans_df['target_calories'].mean()) if not plans_df.empty and 'target_calories' in plans_df else 0.0,
        'ai_generated_plans_count': int((plans_df['ai_generated'] == True).sum()) if not plans_df.empty and 'ai_generated' in plans_df else 0,
        'average_bmi': float(bmi_df['bmi'].mean()) if not bmi_df.empty and 'bmi' in bmi_df else 0.0,
        'event_distribution': events_df['event_name'].value_counts().to_dict() if not events_df.empty else {},
    }

    # 3. LOAD
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    out_json = EXPORT_DIR / 'analytics_warehouse_summary.json'
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(transformed_summary, f, indent=2)

    logger.info("ETL Pipeline completed successfully: %s", transformed_summary)
    return transformed_summary
