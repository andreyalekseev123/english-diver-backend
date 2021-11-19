from rest_framework import serializers

from apps.training import models


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Word
        fields = (
            "id",
            "english",
            "russian",
        )


class UserWordSerializer(serializers.ModelSerializer):
    word = WordSerializer(required=False, read_only=True)

    class Meta:
        model = models.UserWord
        fields = (
            "id",
            "word",
            "rank",
        )


class UserWordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserWord
        fields = (
            "id",
            "word",
        )
