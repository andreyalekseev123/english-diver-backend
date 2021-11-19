import factory.django
from . import models
from ..users.factories import UserFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = models.Category
        django_get_or_create = ("name",)


class WordFactory(factory.django.DjangoModelFactory):
    english = factory.Faker("word")
    russian = factory.Faker("word", locale="ru_RU")

    class Meta:
        model = models.Word
        django_get_or_create = ("english",)


class UserWordFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    word = factory.SubFactory(WordFactory)

    class Meta:
        model = models.UserWord


class UserWithWordsFactory(UserFactory):
    words = factory.RelatedFactoryList(
        UserWordFactory,
        factory_related_name='user',
    )
