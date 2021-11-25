from django_filters import rest_framework as filters

from apps.training.models import Category, Word


class WordsFilter(filters.FilterSet):
    """Filter for words."""
    category = filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        field_name="categories",
    )

    class Meta:
        model = Word
        fields = (
            "category",
        )
