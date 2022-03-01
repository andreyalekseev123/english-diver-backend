"""Here we store information about training types and their ids.

id should not be editable, but other fields could be edit in future, using admin
or other places.

Also here we store info about processing classes for training types
"""
from . import training_types_handlers

WORD_TRANSLATE_ID = "word-translate"
FAST_TRANSLATE_ID = "fast-translate"
WORD_CONSTRUCTOR_ID = "word-constructor"
MULTI_TRAINING_ID = "multi-training"

TRAINING_TYPES = [
    dict(
        id=WORD_TRANSLATE_ID,
        name="Слово-перевод",
        questions_count=5,
        words_per_question_count=4,
        cost=5,
    ),
    dict(
        id=FAST_TRANSLATE_ID,
        name="Перевод на скорость",
        words_can_be_chosen=False,
        questions_count=20,
        words_per_question_count=1,
        cost=2,
    ),
    dict(
        id=WORD_CONSTRUCTOR_ID,
        name="Конструктор слов",
        questions_count=5,
        words_per_question_count=0,
        cost=5,
    ),
    dict(
        id=MULTI_TRAINING_ID,
        name="Мульти тренировка",
        questions_count=5,
        words_per_question_count=4,
        cost=5,
    ),
]

TRAINING_TYPES_PROCESSORS_MAPPING = {
    WORD_TRANSLATE_ID: training_types_handlers.WordTranslateHandler,
    FAST_TRANSLATE_ID: training_types_handlers.FastTranslateHandler,
    WORD_CONSTRUCTOR_ID: training_types_handlers.WordConstructorHandler,
    MULTI_TRAINING_ID: training_types_handlers.MultiTrainingHandler,
}
