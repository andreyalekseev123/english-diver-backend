from collections import namedtuple

from django.utils.translation import gettext_lazy as _

from apps.training import models
from apps.users.models import User

TrainingQuestionData = namedtuple(
    typename="TrainingQuestionData",
    field_names=[
        "word",
        "translation",
        "similar_words",
    ],
)


class BaseTrainingTypeHandler:
    """Base training type handler."""

    WORD_ATTR = "russian"
    TRANSLATE_ATTR = "english"

    def __init__(
        self,
        training_type: models.TrainingType,
        user: User,
    ):
        """Store training type and user."""
        self.training_type = training_type
        self.user = user

    def check_enough_words(self) -> bool:
        """Check that there are enough words in dictionary."""
        return (
            self.user.user_words.count() > self.training_type.questions_count
        )

    def get_not_enough_words_error_message(self) -> str:
        """Get message that should be displayed if not enough words."""
        return _(
            "Not enough words in dictionary. "
            f"There must be at least {self.training_type.questions_count}.",
        )

    def generate_data_for_training(self) -> list[TrainingQuestionData]:
        """Generate data for training."""
        data = []
        questions = self._get_training_questions()
        for question in questions:
            data.append(TrainingQuestionData(
                word=self._get_training_question_data_word(
                    question,
                ),
                translation=self._get_training_question_data_translation(
                    question,
                ),
                similar_words=self._get_similar_words(
                    word=question.user_word.word,
                ),
            ))
        return data

    def _get_training_questions(self) -> list[models.Question]:
        """Get training questions.

        If there is already created training, take questions from it,
        otherwise generate questions.
        """
        training: models.Training = self.training_type.trainings.filter(
            user=self.user,
        ).first()
        if training:
            questions = training.questions.all().select_related(
                "user_word",
                "user_word__word",
            )
        else:
            training = models.Training.objects.create(
                user=self.user,
                type=self.training_type,
            )
            questions = self._generate_training_questions(training)
        return questions

    def _generate_training_questions(
        self,
        training: models.Training,
    ) -> list[models.Question]:
        """Generate questions for training."""
        questions = []
        for user_word in self._get_words_for_training():
            questions.append(models.Question(
                training=training,
                user_word=user_word,
            ))
        models.Question.objects.bulk_create(
            objs=questions,
        )
        return questions

    def _get_similar_words(
        self,
        word: models.Word,
    ) -> list[str]:
        """Get words similar to passed.

        It trying to get similar words using postgres `trigram similar`,
        if found words count less than passed count,
         then gets words from categories.
        """
        count = self.training_type.words_per_question_count
        similar_words = list(
            models.Word.objects.exclude(**{
                self.TRANSLATE_ATTR: getattr(word, self.TRANSLATE_ATTR),
            }).filter(**{
                f"{self.TRANSLATE_ATTR}__trigram_similar":
                    getattr(word, self.TRANSLATE_ATTR),
            })[:count].values_list(self.TRANSLATE_ATTR, flat=True)
        )
        remaining_count = count - len(similar_words)
        if remaining_count > 0:
            qs = models.Word.objects.exclude(english=word.english).filter(
                categories__in=word.categories.values("id"),
            ).order_by('?')[:remaining_count]

            similar_words += list(qs.values_list(
                self.TRANSLATE_ATTR,
                flat=True,
            ))
        return similar_words

    def _get_words_for_training(self) -> list[models.UserWord]:
        """Get words for training questions.

        Firstly it tries to get words from added to training words, check
        `TrainingTypeUserWord` processing.
        If not enough words, then it get another words from dictionary
        """
        chosen_words = self.user.user_words.filter(
            chosen_words__training_type=self.training_type,
        ).order_by("rank")[:self.training_type.questions_count]

        chosen_words_count = chosen_words.count()
        additional_words = []
        if chosen_words_count != self.training_type.questions_count:
            remaining_count = (
                    self.training_type.questions_count - chosen_words_count
            )
            additional_words = self._get_additional_words_for_training(
                chosen_words=chosen_words,
                remaining_count=remaining_count,
            )
        return list(chosen_words) + list(additional_words)

    def _get_additional_words_for_training(
        self,
        chosen_words: list[models.UserWord],
        remaining_count: int,
    ) -> list[models.UserWord]:
        """Override this to get words that need for training type.

        This need if not enough words in chosen words.
        """
        return self.user.user_words.exclude(
            id__in=chosen_words,
        ).order_by("rank")[:remaining_count]

    def _get_training_question_data_word(
        self,
        question: models.Question,
    ) -> str:
        """Override this get word that presented to user."""
        return getattr(question.user_word.word, self.WORD_ATTR)

    def _get_training_question_data_translation(
        self,
        question: models.Question,
    ) -> dict:
        """Override this get translation of word that presented to user."""
        return dict(
            word=getattr(question.user_word.word, self.TRANSLATE_ATTR),
            image=question.user_word.word.image,
        )
