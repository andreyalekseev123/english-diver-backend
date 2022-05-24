from rest_framework.mixins import ListModelMixin

from apps.core.api.views import BaseViewSet
from apps.training.api.filters import WordsFilter
from apps.training.api.serializers import WordSerializer
from apps.training.models import Word


class WordsViewSet(BaseViewSet, ListModelMixin):
    """ViewSet for words with filtering.

    It can be used to get words for category.
    """
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    filterset_class = WordsFilter

    search_fields = (
        "english",
        "russian",
    )

    def get_queryset(self):
        """Annotate with is_linked."""
        return super().get_queryset().with_is_linked(self.request.user).order_by("english")
