from django.urls import path
from .views import (
    ExportListView,
    ExportDownloadView,
    ExportZipDownloadView,
    ExportReSyncView,
    ActivityLogListView,
    LoginHistoryListView,
)

from .admin_views import (
    AdminAnalyticsView,
    AdminUserManagementView,
    AdminAILogsView,
    AdminSystemMonitorView,
)

urlpatterns = [
    path('exports/', ExportListView.as_view(), name='export-list'),
    path('exports/download/', ExportDownloadView.as_view(), name='export-download'),
    path('exports/download-zip/', ExportZipDownloadView.as_view(), name='export-zip'),
    path('exports/sync/', ExportReSyncView.as_view(), name='export-sync'),
    path('activity-logs/', ActivityLogListView.as_view(), name='activity-logs'),
    path('login-history/', LoginHistoryListView.as_view(), name='login-history'),

    # Admin Dashboard Endpoints
    path('admin/analytics/', AdminAnalyticsView.as_view(), name='admin-analytics'),
    path('admin/users/', AdminUserManagementView.as_view(), name='admin-users'),
    path('admin/ai-logs/', AdminAILogsView.as_view(), name='admin-ai-logs'),
    path('admin/system/', AdminSystemMonitorView.as_view(), name='admin-system'),
]
