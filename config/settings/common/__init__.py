import mimetypes

from .authentication import *
from .celery import *
from .drf import *
from .installed_apps import *
from .imagekit import *
from .internationalization import *
from .middleware import *
from .paths import *
from .static import *
from .templates import *

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = 1
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

ADMINS = (
    ("Andrey Alekseev", "andreyaletor2001@gmail.com"),
)

ALLOWED_HOSTS = ['*']
TESTING = False