from import_export import widgets
from import_export.resources import ModelResource as BaseModelResource

from apps.core.import_export.widgets import CharWidget


class ModelResource(BaseModelResource):
    """Override to add custom widgets."""

    WIDGETS_MAP = {
        'ManyToManyField': 'get_m2m_widget',
        'OneToOneField': 'get_fk_widget',
        'ForeignKey': 'get_fk_widget',
        'DecimalField': widgets.DecimalWidget,
        'DateTimeField': widgets.DateTimeWidget,
        'DateField': widgets.DateWidget,
        'TimeField': widgets.TimeWidget,
        'DurationField': widgets.DurationWidget,
        'FloatField': widgets.FloatWidget,
        'IntegerField': widgets.IntegerWidget,
        'PositiveIntegerField': widgets.IntegerWidget,
        'BigIntegerField': widgets.IntegerWidget,
        'PositiveSmallIntegerField': widgets.IntegerWidget,
        'SmallIntegerField': widgets.IntegerWidget,
        'SmallAutoField': widgets.IntegerWidget,
        'AutoField': widgets.IntegerWidget,
        'BigAutoField': widgets.IntegerWidget,
        'NullBooleanField': widgets.BooleanWidget,
        'BooleanField': widgets.BooleanWidget,
        'CICharField': CharWidget,
    }
