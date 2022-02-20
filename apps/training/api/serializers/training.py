from operator import itemgetter

from django.db.models import F
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.core.api.serializers import BaseSerializer

from ... import models


class TrainingItemSerializer(BaseSerializer):
    """Serializer for training item."""
    russian = serializers.CharField()
    translation = serializers.CharField()
    words = serializers.ListField(
        child=serializers.CharField(),
    )


class FinishTrainingItemSerializer(BaseSerializer):
    """Serializer for finish training item."""
    word = serializers.CharField()
    is_true = serializers.BooleanField()

    def validate_word(self, word: str):
        """Validate if this word was in training"""
        training = self._parent_from_list.training
        current_training_words = [
            question.user_word.word.english for question
            in training.questions.all()
        ]
        if word not in current_training_words:
            raise serializers.ValidationError(
                _(f"{word} wasn't in training"),
            )
        return word


class FinishTrainingSerializer(BaseSerializer):
    """Serializer to finish training"""
    result = FinishTrainingItemSerializer(many=True)

    def __init__(
        self,
        training: models.Training = None,
        *args,
        **kwargs,
    ):
        """Override to store current training words."""
        self.training = training
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        """Validate all words were passed."""
        attrs = super().validate(attrs)
        result = attrs["result"]
        words = [data["word"] for data in result]
        current_training_words = [
            question.user_word.word.english for question
            in self.training.questions.all()
        ]
        current_training_words.sort()
        words.sort()
        if words != current_training_words:
            raise serializers.ValidationError(
                _("Not all words were provided"),
            )
        return attrs

    def save(self, **kwargs):
        """Update words ranks.

        Also it deletes questions to start new training.
        """
        result = self.validated_data["result"]
        right_words = list(filter(
            itemgetter("is_true"),
            result,
        ))
        right_words_ids = [result_item["word"] for result_item in right_words]
        if len(right_words_ids) > 0:
            models.UserWord.objects.filter(
                user=self._user,
                word_id__in=right_words_ids,
            ).update(
                rank=F("rank") + self.training.type.cost,
            )
            models.TrainingTypeUserWord.objects.filter(
                training_type=self.training.type,
                user_word__user=self._user,
                user_word__word_id__in=right_words_ids,
            ).delete()
            self.training.delete()
