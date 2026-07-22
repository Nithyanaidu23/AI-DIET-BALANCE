from django.contrib import admin
from django.http import HttpResponse
from .models import LoginHistory, ActivityLog
from .exporter import export_all, create_export_zip_buffer


@admin.action(description="Export all data to CSV and JSON files")
def trigger_export_action(modeladmin, request, queryset):
    export_all()
    modeladmin.message_user(request, "Successfully exported all data to exports/ folder in CSV and JSON formats.")


@admin.action(description="Download ZIP archive of all export files")
def download_zip_action(modeladmin, request, queryset):
    zip_buffer = create_export_zip_buffer()
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="ai_diet_planner_exports.zip"'
    return response


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'login_time', 'logout_time', 'ip_address', 'browser_name', 'os_name', 'device_type', 'status')
    list_filter = ('status', 'device_type', 'os_name', 'browser_name', 'login_time')
    search_fields = ('user_email', 'user_name', 'ip_address', 'session_id')
    readonly_fields = ('login_time',)
    actions = [trigger_export_action, download_zip_action]


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'description', 'ip_address', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__email', 'description', 'ip_address')
    readonly_fields = ('timestamp',)
    actions = [trigger_export_action, download_zip_action]
