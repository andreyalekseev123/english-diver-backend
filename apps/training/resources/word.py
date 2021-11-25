from import_export import resources

from apps.core.import_export.fields import FieldWithAddM2M
from apps.core.import_export.widgets import CreatableManyToManyWidget

from .. import models


class WordResource(resources.ModelResource):
    """Resource for word importing/exporting."""
    categories = FieldWithAddM2M(
        attribute="categories",
        column_name="Categories",
        widget=CreatableManyToManyWidget(
            model=models.Category,
            field="name"
        )
    )

    class Meta:
        model = models.Word
        use_transactions = True
        import_id_fields = (
            "english",
        )
        fields = (
            "id",
            "english",
            "russian",
            "categories",
        )
