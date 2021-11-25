from rest_framework import serializers

from apps.core.api.serializers import ModelBaseSerializer
from apps.training import models


class WordSerializer(ModelBaseSerializer):
    class Meta:
        model = models.Word
        fields = (
            "id",
            "english",
            "russian",
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


class CategoryIdSerializer(serializers.Serializer):
    """Serializer for category id."""
    category_id = serializers.IntegerField()
