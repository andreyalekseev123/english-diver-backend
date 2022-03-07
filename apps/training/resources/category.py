from import_export import resources
from import_export.fields import Field

from libs.import_export.widgets import FileWidget
from .. import models


class CategoryResource(resources.ModelResource):
    """Resource for word importing/exporting."""
    image = Field(
        column_name="image",
        widget=FileWidget(filename="image")
    )

    class Meta:
        model = models.Category
        use_transactions = True
        fields = (
            "id",
            "name",
            "image",
        )
