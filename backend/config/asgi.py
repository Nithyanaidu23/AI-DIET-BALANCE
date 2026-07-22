"""ASGI config for AI Diet Planner."""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
application = get_asgi_application()
