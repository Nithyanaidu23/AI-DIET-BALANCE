"""
Settings file for load testing — inherits from base configuration
but configures production-like options (PostgreSQL, connection pooling, debug=False)
while explicitly bypassing rate limiting/throttling and enabling mock LLM services.
"""
from decouple import config
import dj_database_url
from .base import *

# ─── Load Test Flag ───────────────────────────────────────────────────────────
LOAD_TEST = True

# ─── Debug & Security ─────────────────────────────────────────────────────────
DEBUG = False

# Ensure any host can access the API during local dockerized tests
ALLOWED_HOSTS = ['*']

# ─── Database Configuration ───────────────────────────────────────────────────
# Inherit production PostgreSQL configurations if DATABASE_URL is set (e.g. Docker)
DATABASE_URL = config('DATABASE_URL', default='')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ─── Disable Throttling / Rate Limits ─────────────────────────────────────────
if 'REST_FRAMEWORK' in globals():
    REST_FRAMEWORK = REST_FRAMEWORK.copy()
    REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []
    REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {}

# ─── Mock Email Backend for Safety ────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
