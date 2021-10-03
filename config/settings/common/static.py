# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
import os

from .paths import BASE_DIR

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / "static"
JS_REVERSE_OUTPUT_PATH = BASE_DIR / "assets"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "assets"),
)
