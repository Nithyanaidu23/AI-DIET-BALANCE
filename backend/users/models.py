"""UserProfile model — extended user data for diet planning."""
from django.conf import settings
from django.db import models


class ActivityLevel(models.TextChoices):
    SEDENTARY = 'sedentary', 'Sedentary (little or no exercise)'
    LIGHT = 'light', 'Lightly Active (1-3 days/week)'
    MODERATE = 'moderate', 'Moderately Active (3-5 days/week)'
    VERY = 'very', 'Very Active (6-7 days/week)'
    EXTRA = 'extra', 'Extra Active (physical job or 2x training)'


class Gender(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    OTHER = 'other', 'Other'
    PREFER_NOT = 'prefer_not_to_say', 'Prefer not to say'


class FitnessGoal(models.TextChoices):
    LOSE_FAT = 'lose_fat', 'Lose Fat'
    BUILD_MUSCLE = 'build_muscle', 'Build Muscle'
    MAINTAIN = 'maintain', 'Maintain Weight'
    IMPROVE_HEALTH = 'improve_health', 'Improve Overall Health'
    INCREASE_ENDURANCE = 'increase_endurance', 'Increase Endurance'


class FoodPreference(models.TextChoices):
    NONE = 'none', 'No Preference'
    VEGETARIAN = 'vegetarian', 'Vegetarian'
    VEGAN = 'vegan', 'Vegan'
    PESCATARIAN = 'pescatarian', 'Pescatarian'
    KETO = 'keto', 'Keto'
    PALEO = 'paleo', 'Paleo'
    MEDITERRANEAN = 'mediterranean', 'Mediterranean'
    GLUTEN_FREE = 'gluten_free', 'Gluten-Free'


class UserProfile(models.Model):
    """Extended profile linked 1:1 to the User model."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    # Physical stats
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)

    # Lifestyle
    activity_level = models.CharField(
        max_length=20, choices=ActivityLevel.choices, default=ActivityLevel.MODERATE
    )
    fitness_goal = models.CharField(
        max_length=30, choices=FitnessGoal.choices, default=FitnessGoal.MAINTAIN
    )
    food_preference = models.CharField(
        max_length=30, choices=FoodPreference.choices, default=FoodPreference.NONE
    )

    # Health
    allergies = models.TextField(blank=True, help_text='Comma-separated list of allergies.')
    medical_conditions = models.TextField(blank=True, help_text='Comma-separated medical conditions.')

    # Additional preferences
    country = models.CharField(max_length=100, blank=True)
    cuisine_preference = models.CharField(max_length=100, blank=True)
    budget_per_day_usd = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    workout_time = models.CharField(max_length=50, blank=True, help_text='e.g., Morning, Evening')

    # Profile image
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'Profile of {self.user.email}'

    @property
    def allergies_list(self):
        """Return allergies as a Python list."""
        return [a.strip() for a in self.allergies.split(',') if a.strip()]

    @property
    def medical_conditions_list(self):
        return [c.strip() for c in self.medical_conditions.split(',') if c.strip()]

    @property
    def is_complete(self):
        """Check if the minimum required fields are filled."""
        return all([self.age, self.height_cm, self.weight_kg, self.gender])


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} — {self.title}'


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_entries')
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback Entries'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} — {self.rating} stars'

