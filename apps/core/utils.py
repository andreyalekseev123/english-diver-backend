from drf_spectacular.utils import extend_schema, extend_schema_view


def define_swagger_extend_schema(
    view,
    method,
    tags=None,
    operation_id=None,
    operation_description=None,
    operation_summary=None,
    request_body=None,
    parameters=None,
    responses=None,
    **kwargs
):
    """Function to define hooks for swagger autoschema

    This is simple shortcut wrapper on `extend_schema`, which passed
    most params to it.

    It needed to have single place for schema defining
    """
    extend_schema_view(**{
        method: extend_schema(
            tags=tags,
            operation_id=operation_id,
            description=operation_description,
            summary=operation_summary,
            request=request_body,
            parameters=parameters,
            responses=responses,
            **kwargs,
        ),
    })(view)
