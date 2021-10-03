import os

from django.conf import settings

from celery import Celery
from post_request_task.task import PostRequestTask

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery(
    "english-diver",
    task_cls=PostRequestTask,
)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
