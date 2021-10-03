import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TrainingType(models.Model):
    """Type of training."""
    name = models.CharField(
        max_length=255,
        verbose_name=_("Type Name"),
    )
    cost = models.PositiveIntegerField(
        verbose_name=_("Training Type Cost"),
        validators=[MaxValueValidator(100)]
    )

    class Meta:
        verbose_name = _("Training Type")
        verbose_name_plural = _("Training Types")
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}({self.cost})"


class Training(models.Model):
    """Training of user."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="trainings",
        related_query_name="training",
    )
    type = models.ForeignKey(
        "training.TrainingType",
        on_delete=models.RESTRICT,
        related_name="trainings",
    )

    class Meta:
        verbose_name = _("Training")
        verbose_name_plural = _("Trainings")

    def __str__(self):
        return f"{self.user} training: {self.type}"


class Question(models.Model):
    """Question for training."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    training = models.ForeignKey(
        "training.Training",
        on_delete=models.CASCADE,
        related_name="questions",
        null=False,
    )
    user_word = models.ForeignKey(
        "training.UserWord",
        on_delete=models.RESTRICT,
        null=False,
    )

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        unique_together = ("training", "user_word")

    def __str__(self):
        return f"Question for {self.training}: {self.user_word}"

    def clean(self):
        """Check that user word related to user which started training."""
        if self.user_word.user != self.training.user:
            raise ValidationError(
                f"UserWord must relate to {self.training.user}",
            )
