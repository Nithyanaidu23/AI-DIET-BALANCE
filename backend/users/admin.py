from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'weight_kg', 'height_cm', 'fitness_goal', 'activity_level', 'updated_at')
    list_filter = ('fitness_goal', 'activity_level', 'food_preference', 'gender')
    search_fields = ('user__email', 'user__first_name')
    readonly_fields = ('created_at', 'updated_at')
