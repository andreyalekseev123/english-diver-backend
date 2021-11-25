from import_export.fields import Field


class FieldWithAddM2M(Field):
    """Custom class that uses add for M2M."""

    def save(self, obj, data, is_m2m=False, **kwargs):
        """Override to use add instead of set for M2M."""
        if not self.readonly:
            attrs = self.attribute.split('__')
            for attr in attrs[:-1]:
                obj = getattr(obj, attr, None)
            cleaned = self.clean(data, **kwargs)
            if cleaned is not None or self.saves_null_values:
                if not is_m2m:
                    setattr(obj, attrs[-1], cleaned)
                else:
                    getattr(obj, attrs[-1]).add(*cleaned)