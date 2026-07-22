"""Health app models — BMI records and water tracking."""
from django.conf import settings
from django.db import models


class BMIRecord(models.Model):
    """Timestamped BMI snapshot for tracking user progress over time."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bmi_records'
    )
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1)
    height_cm = models.DecimalField(max_digits=5, decimal_places=1)
    bmi = models.DecimalField(max_digits=4, decimal_places=1)
    bmi_category = models.CharField(max_length=30)
    body_fat_percent = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    ideal_weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    goal_calories = models.IntegerField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'BMI Record'
        verbose_name_plural = 'BMI Records'
        ordering = ['-recorded_at']

    def __str__(self):
        return f'{self.user.email} — BMI {self.bmi} ({self.recorded_at.date()})'


class WaterTracker(models.Model):
    """Daily water intake log."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='water_logs'
    )
    date = models.DateField()
    amount_ml = models.PositiveIntegerField(default=0)
    target_ml = models.PositiveIntegerField(default=2500)

    class Meta:
        unique_together = ('user', 'date')
        verbose_name = 'Water Log'
        verbose_name_plural = 'Water Logs'
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.email} — {self.date}: {self.amount_ml}ml / {self.target_ml}ml'

    @property
    def percent_complete(self):
        if self.target_ml == 0:
            return 0
        return round((self.amount_ml / self.target_ml) * 100, 1)


class ExerciseLog(models.Model):
    """Exercise and workout tracking."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exercise_logs'
    )
    exercise_name = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField(default=30)
    calories_burned = models.PositiveIntegerField(default=0)
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Exercise Log'
        verbose_name_plural = 'Exercise Logs'
        ordering = ['-logged_at']

    def __str__(self):
        return f'{self.user.email} — {self.exercise_name} ({self.duration_minutes}m, {self.calories_burned} kcal)'

