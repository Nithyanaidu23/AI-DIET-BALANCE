"""
Django Signals for automatic LoginHistory, ActivityLog, and Export synchronization.
"""
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import LoginHistory, ActivityLog, ActionType, LoginStatus
from .exporter import export_all

User = get_user_model()


def log_activity(user, action: str, description: str = '', ip_address: str = ''):
    """Helper to log an activity and trigger export sync."""
    try:
        ActivityLog.objects.create(
            user=user if user and user.is_authenticated else None,
            action=action,
            description=description,
            ip_address=ip_address,
        )
    except Exception as e:
        import logging
        logging.getLogger('activity_logs').error(f"Failed to record ActivityLog: {e}")


def log_event(user, event_name: str, metadata: dict = None):
    """Record an event into the events table for analytics pipeline."""
    try:
        from .models import AnalyticsEvent
        AnalyticsEvent.objects.create(
            user=user if user and user.is_authenticated else None,
            event_name=event_name,
            metadata=metadata or {},
        )
    except Exception as e:
        import logging
        logging.getLogger('activity_logs').error(f"Failed to record AnalyticsEvent: {e}")



@receiver(user_logged_in)
def handle_user_logged_in(sender, request, user, **kwargs):
    audit_meta = getattr(request, 'audit_meta', {})
    ip = audit_meta.get('ip', '127.0.0.1')
    ua = audit_meta.get('user_agent', '')
    browser = audit_meta.get('browser', 'Unknown Browser')
    os_name = audit_meta.get('os', 'Unknown OS')
    device = audit_meta.get('device', 'Desktop')
    session = getattr(request, 'session', None)
    session_key = getattr(session, 'session_key', '') or '' if session else ''

    # Record LoginHistory
    LoginHistory.objects.create(
        user=user,
        user_email=user.email,
        user_name=user.full_name,
        login_time=timezone.now(),
        ip_address=ip,
        user_agent=ua,
        device_type=device,
        os_name=os_name,
        browser_name=browser,
        session_id=session_key,
        status=LoginStatus.SUCCESS,
    )

    # Record ActivityLog
    log_activity(user, ActionType.LOGIN, description=f"User logged in from {ip} ({browser} on {os_name})", ip_address=ip)

    # Sync exports
    export_all()


@receiver(user_logged_out)
def handle_user_logged_out(sender, request, user, **kwargs):
    if user and user.is_authenticated:
        # Update logout time on latest LoginHistory
        latest_login = LoginHistory.objects.filter(user=user, logout_time__isnull=True).first()
        if latest_login:
            latest_login.logout_time = timezone.now()
            latest_login.save(update_fields=['logout_time'])

        ip = getattr(request, 'audit_meta', {}).get('ip', '')
        log_activity(user, ActionType.LOGOUT, description="User logged out", ip_address=ip)

    export_all()


@receiver(post_save, sender=User)
def handle_user_saved(sender, instance, created, **kwargs):
    if created:
        log_activity(instance, ActionType.USER_REGISTERED, description=f"New user registered: {instance.email}")
    export_all()


def setup_all_export_signals():
    """Import models and connect post_save for all audited entities."""
    from users.models import UserProfile
    from nutrition.models import Food
    from mealplanner.models import MealPlan
    from health.models import BMIRecord, WaterTracker

    def generic_post_save(sender, instance, **kwargs):
        try:
            export_all()
        except Exception:
            pass

    for model in [UserProfile, Food, MealPlan, BMIRecord, WaterTracker, LoginHistory, ActivityLog]:
        post_save.connect(generic_post_save, sender=model, weak=False)
