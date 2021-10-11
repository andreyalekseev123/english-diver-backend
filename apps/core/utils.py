from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema, unset


def define_swagger_auto_schema(
    view,
    method,
    tags=None,
    operation_id=None,
    operation_description=None,
    operation_summary=None,
    auto_schema=unset,
    request_body=None,
    query_serializer=None,
    manual_parameters=None,
    responses=None,
    field_inspectors=None,
    filter_inspectors=None,
    paginator_inspectors=None,
    **kwargs
):
    """Function to define hooks for swagger autoschema

    This is simple shortcut wrapper on `swagger_auto_schema`, which passed
    most params to it.

    It needed to have single place for schema defining
    """
    method_decorator(
        name=method,
        decorator=swagger_auto_schema(
            tags=tags,
            operation_id=operation_id,
            operation_description=operation_description,
            operation_summary=operation_summary,
            auto_schema=auto_schema,
            request_body=request_body,
            query_serializer=query_serializer,
            manual_parameters=manual_parameters,
            responses=responses,
            field_inspectors=field_inspectors,
            filter_inspectors=filter_inspectors,
            paginator_inspectors=paginator_inspectors,
            **kwargs,
        )
    )(view)
