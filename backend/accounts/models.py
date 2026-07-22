"""Custom User model using email as the primary identifier."""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Manager for the custom User model."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required.')
        email = self.normalize_email(email)
        pwd = password or extra_fields.pop('password', None)
        user = self.model(email=email, **extra_fields)
        if pwd:
            user.set_password(pwd)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class RoleChoices(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    USER = 'user', 'User'


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model.
    Uses email instead of username for authentication.
    Supports explicit role-based access control (Admin vs User).
    """
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
        db_index=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    # Google OAuth stub fields
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    avatar_url = models.URLField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    @property
    def full_name(self) -> str:
        name = f"{self.first_name} {self.last_name}".strip()
        return name if name else self.email

    @property
    def is_admin(self) -> bool:
        return self.role == RoleChoices.ADMIN or self.is_staff or self.is_superuser

    def save(self, *args, **kwargs):
        if self.is_staff or self.is_superuser:
            self.role = RoleChoices.ADMIN
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.email} ({self.role})"


class PlanType(models.TextChoices):
    FREE = 'free', 'Free Tier'
    PRO = 'pro', 'Pro Tier ($9.99/mo)'
    ENTERPRISE = 'enterprise', 'Enterprise ($29.99/mo)'


class SubscriptionStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    CANCELED = 'canceled', 'Canceled'
    PAST_DUE = 'past_due', 'Past Due'
    EXPIRED = 'expired', 'Expired'


class Subscription(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=20, choices=PlanType.choices, default=PlanType.FREE)
    status = models.CharField(max_length=20, choices=SubscriptionStatus.choices, default=SubscriptionStatus.ACTIVE)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    current_period_start = models.DateTimeField(default=timezone.now)
    current_period_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return f"{self.user.email} — {self.plan} ({self.status})"


class Payment(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    stripe_charge_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default='succeeded')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']

    def __str__(self):
        return f"${self.amount} {self.currency} by {self.user.email} on {self.created_at.date()}"

