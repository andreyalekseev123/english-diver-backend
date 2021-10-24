from rest_framework import status

from apps.core.utils import define_swagger_extend_schema

from .serializers import PasswordResetConfirmSerializer, UserSerializer
from .views import (
    PasswordResetConfirmView,
    PasswordResetView,
    RegistrationAPIView,
)

define_swagger_extend_schema(
    view=RegistrationAPIView,
    method='post',
    responses={status.HTTP_201_CREATED: UserSerializer}
)

define_swagger_extend_schema(
    view=PasswordResetView,
    method='post',
    responses=None
)
define_swagger_extend_schema(
    view=PasswordResetConfirmView,
    method='post',
    responses=None,
    request_body=PasswordResetConfirmSerializer
)

