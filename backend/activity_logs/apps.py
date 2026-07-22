from django.apps import AppConfig


class ActivityLogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'activity_logs'

    def ready(self):
        try:
            import activity_logs.signals  # noqa
            activity_logs.signals.setup_all_export_signals()
        except Exception:
            pass
