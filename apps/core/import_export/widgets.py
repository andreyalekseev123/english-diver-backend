from import_export.widgets import CharWidget as BaseCharWidget
from import_export.widgets import ManyToManyWidget


class CreatableManyToManyWidget(ManyToManyWidget):
    """Overrides to add object creation."""

    def clean(self, value, row=None, *args, **kwargs):
        instances = super().clean(value, row, *args, **kwargs)
        if instances:
            return instances

        if isinstance(value, (float, int)):
            field_values = [int(value)]
        else:
            field_values = value.split(self.separator)

        instances = []
        for field_value in field_values:
            instances.append(
                self.model.objects.create(
                    **{self.field: field_value}
                )
            )
        return instances


class CharWidget(BaseCharWidget):

    def clean(self, value, row=None, *args, **kwargs):
        """Strip string."""
        return value.strip()
