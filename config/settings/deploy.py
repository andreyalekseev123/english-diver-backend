import sys

from environ import environ

from .common import *

env = environ.Env()

env.read_env(overwrite=False)

DEBUG = env.bool("DEBUG")
ALLOWED_HOSTS = ["*"]
SECRET_KEY = env("SECRET_KEY")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

DATABASES = {
    "default": env.db("DATABASE_URL"),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = 600

CELERY_TASK_ALWAYS_EAGER = env("CELERY_TASK_ALWAYS_EAGER")
CELERY_BROKER_URL = ""
CELERY_RESULT_BACKEND = ""
CELERY_TASK_DEFAULT_QUEUE = ""
# disable django DEBUG if we run celery worker
if "celery" in sys.argv[0]:
    DEBUG = False

# disable any password restrictions
AUTH_PASSWORD_VALIDATORS = []

FRONTEND_DOMAIN = env("FRONTEND_DOMAIN")

CLOUDINARY_CLOUD_NAME = env("CLOUD_NAME")
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,
    "API_KEY": env("API_KEY"),
    "API_SECRET": env("API_SECRET"),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
