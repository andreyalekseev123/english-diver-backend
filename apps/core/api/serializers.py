import copy

from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    """Serializer with common logic."""

    def __init__(self, *args, **kwargs):
        """Set current user."""
        super().__init__(*args, **kwargs)
        self._request = self.context.get("request")
        self._user = getattr(self._request, "user", None)

    @property
    def _parent_from_list(self):
        """Get parent serializer for parent list serializer.

        This could be used to get parent instance when you are using this
        serializer as field.

        Example:
        class ParentSerializer(ModelBaseSerializer):
            children = ChildSerializer(many=True)

        self.parent is ListSerializer which uses ChildSerializer as child,
        while ListSerializer's parent is ParentSerializer.

        """
        return self.parent.parent


class ModelBaseSerializer(BaseSerializer, serializers.ModelSerializer):
    """Model Serializer with common logic."""

    def get_instance(self):
        """Get instance depending on request."""
        if self.instance:  # if it's update request
            return copy.deepcopy(self.instance)
        # pylint: disable=no-member
        return self.Meta.model()  # if it's create request

    def prepare_instance(self, attrs):
        """Prepare instance depending on create/update.

        If `create` used, create empty instance and set fields' values with
        received data.
        If `update` used, update existing instance with received data.

        """
        # Prepare instance depending on create/update
        instance = self.get_instance()

        # Get instance related fields' names
        # pylint: disable=no-member
        relations = getattr(self.Meta, "relations", set())

        # Set new data for instance, while ignoring relations
        for attr, value in attrs.items():
            if attr not in relations:
                setattr(instance, attr, value)

        return instance

    def validate(self, attrs):
        """Call model's `.clean()` method during validation.

        Create:
            Just create model instance using provided data.
        Update:
            `self.instance` contains instance with new data. We apply passed
            data to it and then call `clean` method for this temp instance.

        """
        attrs = super().validate(attrs)

        instance = self.prepare_instance(attrs)

        instance.clean()

        return attrs


# pylint: disable=abstract-method
class BaseListSerializer(serializers.ListSerializer):
    """List Base Serializer with common logic.

    Original `run_validation` returns a dict with `non_field_errors`.
    >>> {'non_field_errors': <raised_error>}

    But since our errors map to the child objects, we replicate
    the behavior when an error occurs in a child serializer:
    >>> [
    ...     {}, # valid
    ...     {'non_field_errors': ['some error']},
    ... ]

    """

    def __init__(self, *args, **kwargs):
        """Set current user."""
        super().__init__(*args, **kwargs)
        self._request = self.context.get("request")
        self._user = getattr(self._request, "user", None)

    def run_validation(self, data=serializers.empty):
        """Override the default `run_validation` to return a list of errors."""
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data

        value = self.to_internal_value(data)
        self.run_validators(value)
        return self.validate(value)
