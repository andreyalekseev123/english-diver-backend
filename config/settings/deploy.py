import sys

from .common import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "english_diver_dev",
        "USER": "english_diver_user",
        "PASSWORD": "password",
        "HOST": "postgres",
        "PORT": "5432",
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": 600,
    },
}

EMAIL_HOST = ""
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = ""

CELERY_BROKER_URL = ""
CELERY_RESULT_BACKEND = ""
CELERY_TASK_DEFAULT_QUEUE = ""
# disable django DEBUG if we run celery worker
if "celery" in sys.argv[0]:
    DEBUG = False