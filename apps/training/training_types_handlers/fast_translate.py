from django.utils.translation import gettext_lazy as _

from apps.training import models
from apps.training.training_types_handlers.base import BaseTrainingTypeHandler

MIN_WORDS_COUNT = 5


class FastTranslateHandler(BaseTrainingTypeHandler):
    """Handler for fast translate training type."""

    WORD_ATTR = "english"
    TRANSLATE_ATTR = "russian"

    def check_enough_words(self) -> bool:
        """There must be at least 5 words to start training."""
        return self.user.user_words.count() > MIN_WORDS_COUNT

    def get_not_enough_words_error_message(self) -> str:
        """Get message that should be displayed if not enough words."""
        return _(
            "Not enough words in dictionary. "
            f"There must be at least {MIN_WORDS_COUNT}.",
        )

    def _get_additional_words_for_training(
        self,
        chosen_words: list[models.UserWord],
        remaining_count: int,
    ) -> list[models.UserWord]:
        """Override to get on learning words firstly.

        This is words which  0 < rank < 100
        """
        on_learning_words = list(
            self.user.user_words.exclude(
                id__in=[chosen_word.id for chosen_word in chosen_words],
            ).filter(
                rank__gt=0,
                rank__lt=100,
            ).order_by("rank")[:remaining_count]
        )
        on_learning_words_count = len(on_learning_words)
        other_words = []
        if on_learning_words_count < remaining_count:
            other_words = super()._get_additional_words_for_training(
                chosen_words=chosen_words + on_learning_words,
                remaining_count=remaining_count - on_learning_words_count,
            )

        return on_learning_words + other_words
