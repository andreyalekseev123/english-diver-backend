# This will make sure the app is always imported when
# Django starts so that shared_task will use this app. See:
# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
from .celery import app as celery_app
