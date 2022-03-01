from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.core.api.serializers import BaseSerializer, ModelBaseSerializer
from apps.training import models


class WordSerializer(ModelBaseSerializer):
    is_linked = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Word
        fields = (
            "id",
            "english",
            "russian",
            "is_linked"
        )


class UserWordSerializer(ModelBaseSerializer):
    word = WordSerializer(required=False, read_only=True)

    class Meta:
        model = models.UserWord
        fields = (
            "id",
            "word",
            "rank",
        )


class UserWordCreateSerializer(ModelBaseSerializer):
    class Meta:
        model = models.UserWord
        fields = (
            "id",
            "word",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        validated_data["user"] = self._user
        return super().create(validated_data)


class UserWordRemoveSerializer(BaseSerializer):
    word = serializers.CharField()

    def validate_word(self, word_id):
        """Validate passed word id.

        Check that word linked to user.
        """
        if not models.Word.objects.filter(
                user_words__user=self._user,
        ).exists():
            raise serializers.ValidationError(
                _("User don't have this word")
            )
        return word_id

    def save(self, **kwargs):
        """Remove word from dictionary.

        Delete training where this word was.
        """
        word_id = self.validated_data["word"]
        models.Training.objects.filter(
            questions__user_word__word_id=word_id,
        ).delete()
        models.UserWord.objects.get(
            user=self._user,
            word_id=word_id,
        ).delete()


class CategoryIdSerializer(serializers.Serializer):
    """Serializer for category id."""
    category_id = serializers.IntegerField()


class AddWordsToTrainingSerializer(BaseSerializer):
    """Serializer to add words to training type for future trainings."""
    words = serializers.PrimaryKeyRelatedField(
        queryset=models.Word.objects.all(),
        many=True,
    )
    training_type = serializers.PrimaryKeyRelatedField(
        queryset=models.TrainingType.objects.all(),
    )

    def validate_words(self, words):
        """Validate that all words are in dictionary."""
        words_in_dictionary_count = self._user.words.filter(
            id__in=[word.id for word in words],
        ).count()
        if len(words) != words_in_dictionary_count:
            raise serializers.ValidationError(
                _("Not all words are in dictionary")
            )
        return words

    def validate(self, attrs):
        """Check that words can be chosen for training type."""
        if not attrs["training_type"].words_can_be_chosen:
            raise serializers.ValidationError(
                _("Words can be chosen for this training type"),
            )
        return attrs

    def save(self, **kwargs):
        """Save words for future trainings.

        Also it deletes created training if no chosen words were in it.
        """
        words = self.validated_data["words"]
        training_type = self.validated_data["training_type"]

        current_training = self._user.trainings.filter(
            type=training_type,
        ).first()
        if current_training:
            current_training_questions = current_training.questions.all()
            if not current_training_questions.filter(
                user_word__chosen_words__training_type=training_type,
            ).exists():
                current_training.delete()

        user_words = self._user.user_words.all().filter(
            word__in=words,
        )
        training_type_user_words = []
        for user_word in user_words:
            training_type_user_words.append(models.TrainingTypeUserWord(
                training_type=training_type,
                user_word=user_word,
            ))
        models.TrainingTypeUserWord.objects.bulk_create(
            objs=training_type_user_words,
            ignore_conflicts=True,
        )
