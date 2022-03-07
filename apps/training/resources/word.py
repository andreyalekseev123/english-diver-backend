
from libs.import_export.widgets import FileWidget

from apps.core.import_export.fields import FieldWithAddM2M
from apps.core.import_export.widgets import CreatableManyToManyWidget

from ...core.import_export.resource import ModelResource
from .. import models


class WordResource(ModelResource):
    """Resource for word importing/exporting."""

    categories = FieldWithAddM2M(
        attribute="categories",
        column_name="Categories",
        widget=CreatableManyToManyWidget(
            model=models.Category,
            field="name"
        )
    )
    image = FileWidget(filename="image")

    class Meta:
        model = models.Word
        use_transactions = True
        import_id_fields = (
            "english",
        )
        fields = (
            "english",
            "russian",
            "image",
            "categories",
        )
