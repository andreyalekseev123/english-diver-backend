from apps.core.api.serializers import ModelBaseSerializer
from apps.training.models import TrainingType


class TrainingTypeSerializer(ModelBaseSerializer):
    """TrainingType for list view."""

    class Meta:
        model = TrainingType
        fields = (
            "id",
            "name",
            "description",
            "image",
            "words_can_be_chosen",
        )
