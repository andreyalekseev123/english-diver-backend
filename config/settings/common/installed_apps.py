# Application definition

DJANGO_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.forms",
)

THIRD_PARTY_APPS = (
    "imagekit",
    "rest_framework",
    "django_extensions",
    "django_celery_beat",
    "django_object_actions",
    "django_filters",
)

LOCAL_APPS = (
    "apps.users",
    "apps.training",
)

INSTALLED_APPS = (
    DJANGO_APPS +
    THIRD_PARTY_APPS +
    LOCAL_APPS
)
