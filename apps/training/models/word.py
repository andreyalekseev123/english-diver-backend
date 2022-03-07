import uuid

from django.conf import settings
from django.contrib.postgres.fields import CICharField
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Case, OuterRef, Q, Subquery, Value, When
from django.utils.translation import gettext_lazy as _

from django_extensions.db.fields import AutoSlugField


class Category(models.Model):
    """The name of words category."""
    name = CICharField(
        verbose_name=_("Name"),
        max_length=255,
        unique=True,
    )
    image = models.ImageField(
        upload_to=settings.DEFAULT_MEDIA_PATH,
        blank=True,
        null=True,
        verbose_name=_("Image"),
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("name",)

    def __str__(self) -> str:
        return str(self.name)


class WordQuerySet(models.QuerySet):
    """QuerySet for Word model"""

    def with_is_linked(self, user):
        """Annotate with `is_linked`.

        Does this user already linked to this word.
        """
        user_words = UserWord.objects.filter(
            word=OuterRef("pk")
        ).filter(
            user=user
        ).values("user_id")
        return self.annotate(user_id=Value(user.id)).annotate(
            is_linked=Case(
                When(
                    user_id__in=Subquery(user_words),
                    then=True,
                ),
                default=False,
                output_field=models.BooleanField(),
            ),
        )


class Word(models.Model):
    """The word with translate."""
    id = AutoSlugField(
        populate_from="english",
        primary_key=True,
        max_length=255,
    )
    english = CICharField(
        verbose_name=_("Word in english"),
        max_length=255,
        unique=True,
    )
    russian = CICharField(
        verbose_name=_("Word in russian"),
        max_length=255,
    )
    image = models.ImageField(
        upload_to=settings.DEFAULT_MEDIA_PATH,
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_("Image"),
    )
    categories = models.ManyToManyField(
        "training.Category",
        related_name="words",
        related_query_name="word",
        blank=False,
    )
    users = models.ManyToManyField(
        "users.User",
        related_name="words",
        related_query_name="word",
        through="UserWord",
    )
    objects = WordQuerySet.as_manager()

    class Meta:
        verbose_name = _("Word")
        verbose_name_plural = _("Words")
        ordering = ("english",)

    def __str__(self) -> str:
        return f"{self.english} - {self.russian}"


class UserWord(models.Model):
    """Intermediate model for user-word relationship.

    Rank says about how user learned this word:
        0 - new word for user
        1-99 - in studying
        100 - studied
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    word = models.ForeignKey(
        "training.Word",
        on_delete=models.RESTRICT,
        related_name="user_words",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_words",
    )
    rank = models.PositiveIntegerField(
        verbose_name=_("Rank"),
        validators=[MaxValueValidator(100)],
        default=0,
    )
    learned_times = models.PositiveIntegerField(
        verbose_name=_("Word learned times"),
        validators=[MaxValueValidator(3)],
        default=0,
    )

    class Meta:
        verbose_name = _("User word")
        verbose_name_plural = _("User words")
        unique_together = ("user", "word")
        ordering = ("rank",)

    def __str__(self):
        return f"{self.user}: {self.word} Rank:{self.rank}/100"
