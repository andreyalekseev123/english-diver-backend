from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from . import views
from .serializers import CategoryIdSerializer

extend_schema_view(
    add_category_words=extend_schema(
        request=CategoryIdSerializer,
        responses={
            200: None
        }
    ),
)(views.DictionaryApiViewSet)
