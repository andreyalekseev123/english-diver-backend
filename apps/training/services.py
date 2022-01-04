from random import randint

from django.db.models import QuerySet

from apps.training import models
from apps.users.models import User


def get_words_for_training(
    user: User,
    num_words: int,
) -> QuerySet[models.UserWord]:
    """Get words for training."""
    words = user.user_words.order_by("rank")[:num_words]
    return words


def generate_training_questions(
    training_type: models.TrainingType,
    user: User,
) -> QuerySet[models.Question]:
    """Generate instances for training."""
    training = models.Training.objects.create(
        user=user,
        type=training_type,
    )
    questions = []
    for user_word in get_words_for_training(
        user=user,
        num_words=training_type.questions_count,
    ):
        questions.append(models.Question(
            training=training,
            user_word=user_word,
        ))
    return models.Question.objects.bulk_create(objs=questions)


def generate_data_for_training(
    questions: QuerySet[models.Question],
    training_type: models.TrainingType,
) -> list[dict]:
    """Generate data for training."""
    data = []
    for question in questions:
        russian = question.user_word.word.russian
        translation = question.user_word.word.english
        words = get_similar_words(
            word=question.user_word.word,
            count=training_type.words_per_question_count,
        )
        data.append(dict(
            russian=russian,
            translation=translation,
            words=words,
        ),
        )
    return data


def get_similar_words(word: models.Word, count: int) -> list[str]:
    """Get words similar to passed.

    It trying to get similar words using postgres `trigram similar`,
    if found words count less than passed count,
     then gets words from categories.
    """
    similar_words = list(
        models.Word.objects.exclude(
            english=word.english,
        ).filter(
            english__trigram_similar=word.english,
        )[:count].values_list("english", flat=True)
     )
    remaining_count = count - len(similar_words)
    if remaining_count > 0:
        qs = models.Word.objects.exclude(english=word.english).filter(
            categories__in=word.categories.values("id"),
        ).order_by('?')[:remaining_count]

        similar_words += list(qs.values_list("english", flat=True))
    return similar_words
