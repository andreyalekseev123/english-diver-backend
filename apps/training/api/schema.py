from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from . import views
from . import serializers

extend_schema_view(
    add_category_words=extend_schema(
        request=serializers.CategoryIdSerializer,
        responses={
            200: None
        }
    ),
)(views.DictionaryApiViewSet)

extend_schema_view(
    start=extend_schema(
        request=None,
        responses={
            200: serializers.TrainingItemSerializer,
        }
    ),
    finish=extend_schema(
        request=serializers.FinishTrainingSerializer,
        responses={
            200: None,
        }
    ),
)(views.TrainingTypeViewSet)

