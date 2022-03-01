from django.utils.translation import gettext_lazy as _

from apps.training import models
from apps.training.training_types_handlers.base import BaseTrainingTypeHandler


class FastTranslateHandler(BaseTrainingTypeHandler):
    """Handler for fast translate training type."""

    WORD_ATTR = "english"
    TRANSLATE_ATTR = "russian"

    def check_enough_words(self) -> bool:
        """Check that there are enough words on learning in dictionary."""
        return (
            self.user.user_words.filter(
                rank__gt=0,
                rank__lt=100,
            ).count() > self.training_type.questions_count
        )

    def get_not_enough_words_error_message(self) -> str:
        """Get message that should be displayed if not enough words."""
        return _(
            "Not enough words in dictionary. "
            f"There must be at least {self.training_type.questions_count}"
            f" words on learning.",
        )

    def _get_additional_words_for_training(
        self,
        chosen_words: list[models.UserWord],
        remaining_count: int,
    ) -> list[models.UserWord]:
        """Override to get on learning words.

        This is words which  0 < rank < 100
        """
        return self.user.user_words.exclude(
            id__in=chosen_words,
        ).filter(
            rank__gt=0,
            rank__lt=100,
        ).order_by("rank")[:remaining_count]
