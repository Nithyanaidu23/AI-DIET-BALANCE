"""Models for Login History and Activity Audit Trail."""
from django.conf import settings
from django.db import models


class LoginStatus(models.TextChoices):
    SUCCESS = 'success', 'Success'
    FAILED = 'failed', 'Failed'


class LoginHistory(models.Model):
    """
    Detailed audit log of every user login attempt.
    Tracks User-Agent, IP, Device, OS, Session, and Status.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='login_history',
        null=True,
        blank=True,
    )
    user_email = models.EmailField(help_text="Email used during login attempt")
    user_name = models.CharField(max_length=255, blank=True)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    device_type = models.CharField(max_length=100, default='Desktop/Unknown')
    os_name = models.CharField(max_length=100, default='Unknown OS')
    browser_name = models.CharField(max_length=100, default='Unknown Browser')
    session_id = models.CharField(max_length=255, blank=True)
    jwt_token_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20,
        choices=LoginStatus.choices,
        default=LoginStatus.SUCCESS,
    )
    failed_login_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Login History'
        verbose_name_plural = 'Login History Logs'
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user_email} at {self.login_time} ({self.status})"


class ActionType(models.TextChoices):
    USER_REGISTERED = 'USER_REGISTERED', 'User Registered'
    LOGIN = 'LOGIN', 'User Logged In'
    LOGOUT = 'LOGOUT', 'User Logged Out'
    PROFILE_UPDATED = 'PROFILE_UPDATED', 'Profile Updated'
    MEAL_GENERATED = 'MEAL_GENERATED', 'Meal Plan Generated'
    PDF_DOWNLOADED = 'PDF_DOWNLOADED', 'PDF Downloaded'
    FAVORITE_ADDED = 'FAVORITE_ADDED', 'Favorite Added'
    WATER_UPDATED = 'WATER_UPDATED', 'Water Intake Updated'
    BMI_CALCULATED = 'BMI_CALCULATED', 'BMI Calculated'
    PASSWORD_CHANGED = 'PASSWORD_CHANGED', 'Password Changed'


class ActivityLog(models.Model):
    """
    Complete system audit trail for all user actions.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activity_logs',
        null=True,
        blank=True,
    )
    action = models.CharField(max_length=50, choices=ActionType.choices)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'
        ordering = ['-timestamp']

    def __str__(self):
        user_str = self.user.email if self.user else 'Anonymous'
        return f"[{self.timestamp}] {user_str} - {self.action}"


class AnalyticsEvent(models.Model):
    """
    Event stream for data collection and analytics pipeline.
    Stores user_id, event_name, timestamp, and arbitrary metadata (JSON).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events',
        null=True,
        blank=True,
    )
    event_name = models.CharField(max_length=100, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'events'
        verbose_name = 'Analytics Event'
        verbose_name_plural = 'Analytics Events'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['event_name']),
            models.Index(fields=['user', 'event_name']),
            models.Index(fields=['user', 'timestamp']),
        ]


    def __str__(self):
        user_str = self.user.email if self.user else 'Anonymous'
        return f"{self.event_name} by {user_str} at {self.timestamp}"

