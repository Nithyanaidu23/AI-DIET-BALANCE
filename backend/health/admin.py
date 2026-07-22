from django.contrib import admin
from .models import BMIRecord, WaterTracker


@admin.register(BMIRecord)
class BMIRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'bmi', 'bmi_category', 'weight_kg', 'body_fat_percent', 'recorded_at')
    list_filter = ('bmi_category',)
    search_fields = ('user__email',)


@admin.register(WaterTracker)
class WaterTrackerAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'amount_ml', 'target_ml', 'percent_complete')
    list_filter = ('date',)
