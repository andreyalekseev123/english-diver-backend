from rest_framework import serializers

from apps.core.api.serializers import ModelBaseSerializer
from apps.training.models import Category


class CategorySerializer(ModelBaseSerializer):
    """Category for list view."""
    words_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "image",
            "words_count",
        )

    def get_words_count(self, obj) -> int:
        """Get count of words in category."""
        return obj.words.count()
