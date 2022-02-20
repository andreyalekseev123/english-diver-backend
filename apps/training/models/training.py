import os
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def training_type_upload_to(model_instance, filename):
    """Function for generation of upload path for Django model instance.

    Generates upload path that contain instance"s model app, model name,
    object"s ID, salt and file name.
    """
    components = model_instance._meta.label_lower.split(".")
    components.append(str(model_instance.name))
    components.append(str(uuid.uuid4()))
    components.append(filename)

    return os.path.join(*components)


class TrainingType(models.Model):
    """Type of training."""
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Type Name"),
    )
    image = models.ImageField(
        upload_to=training_type_upload_to,
        blank=True,
        null=True,
        verbose_name=_("Image"),
    )
    questions_count = models.PositiveIntegerField(
        verbose_name=_("Questions count"),
        help_text=_("How much questions must be in training"),
    )
    words_per_question_count = models.PositiveIntegerField(
        verbose_name=_("Words per question count"),
        help_text=_("How much questions must be in training"),
    )

    cost = models.PositiveIntegerField(
        verbose_name=_("Cost"),
        validators=[MaxValueValidator(100)],
    )

    class Meta:
        verbose_name = _("Training Type")
        verbose_name_plural = _("Training Types")
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}({self.cost})"


class TrainingTypeUserWord(models.Model):
    """Words that user added to training."""
    training_type = models.ForeignKey(
        "training.TrainingType",
        on_delete=models.RESTRICT,
        related_name="chosen_words",
    )
    user_word = models.ForeignKey(
        "training.UserWord",
        on_delete=models.CASCADE,
        related_name="chosen_words",
        related_query_name="chosen_words",
    )

    class Meta:
        verbose_name = _("Training Type User Word")
        verbose_name_plural = _("Training Types User Words")

    def __str__(self):
        return f"{self.user_word} for {self.training_type}"


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
        unique_together = ("user", "type")

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
        related_name="questions",
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
                _(f"UserWord must relate to {self.training.user}"),
            )
