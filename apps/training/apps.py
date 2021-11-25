from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TrainingAppConfig(AppConfig):
    """Default configuration for training app."""
    name = "apps.training"
    verbose_name = _("Trainings")

    def ready(self):
        super().ready()
        from .api import schema # noqa