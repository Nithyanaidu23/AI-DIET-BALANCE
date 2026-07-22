"""Views for Exports management, ZIP downloading, and Activity Log inspection."""
import os
from pathlib import Path
from django.http import HttpResponse, FileResponse, Http404
from django.conf import settings
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .exporter import export_all, create_export_zip_buffer, EXPORT_DIR
from .models import ActivityLog, LoginHistory
from .serializers import ActivityLogSerializer, LoginHistorySerializer


class ExportListView(APIView):
    """
    GET /api/exports/ — List all available export files (CSV & JSON).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        export_all()  # ensure exports are updated
        files = []
        if EXPORT_DIR.exists():
            for p in sorted(EXPORT_DIR.glob('*.*')):
                if p.suffix in ['.csv', '.json']:
                    files.append({
                        'name': p.name,
                        'type': p.suffix[1:].upper(),
                        'size_bytes': p.stat().st_size,
                        'updated_at': p.stat().st_mtime,
                        'download_url': f"/api/exports/download/?file={p.name}",
                    })

        return Response({
            'count': len(files),
            'files': files,
            'zip_download_url': '/api/exports/download-zip/',
        })


class ExportDownloadView(APIView):
    """
    GET /api/exports/download/?file=users.csv
    Download a single export file.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        file_name = request.query_params.get('file')
        if not file_name:
            return Response({'error': 'Parameter "file" is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Sanitize file_name to prevent directory traversal
        clean_name = os.path.basename(file_name)
        target_path = EXPORT_DIR / clean_name

        if not target_path.exists() or not target_path.is_file():
            raise Http404("Export file not found.")

        content_type = 'text/csv' if clean_name.endswith('.csv') else 'application/json'
        response = FileResponse(open(target_path, 'rb'), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{clean_name}"'
        return response


class ExportZipDownloadView(APIView):
    """
    GET /api/exports/download-zip/
    Download all export files bundled into a single ZIP archive.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        zip_buffer = create_export_zip_buffer()
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="ai_diet_planner_exports.zip"'
        return response


class ExportReSyncView(APIView):
    """
    POST /api/exports/sync/
    Trigger immediate resynchronization of all DB models into exports/ directory.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            export_all()
            return Response({'message': 'All export files (CSV & JSON) resynchronized successfully.'})
        except Exception as exc:
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ActivityLogListView(generics.ListAPIView):
    """
    GET /api/activity-logs/ — List activity log entries.
    Admins see all logs; regular users see their own.
    """
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ActivityLog.objects.all().select_related('user')
        return ActivityLog.objects.filter(user=user).select_related('user')


class LoginHistoryListView(generics.ListAPIView):
    """
    GET /api/login-history/ — List login history logs.
    Admins see all logs; regular users see their own.
    """
    serializer_class = LoginHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LoginHistory.objects.all().select_related('user')
        return LoginHistory.objects.filter(user=user).select_related('user')
