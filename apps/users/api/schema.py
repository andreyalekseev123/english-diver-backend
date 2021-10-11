from rest_framework import status

from rest_framework_simplejwt import views as jwt_views

from apps.core.utils import define_swagger_auto_schema

from .serializers import TokenObtainPairResponseSerializer, UserSerializer
from .views import RegistrationAPIView

define_swagger_auto_schema(
    view=jwt_views.TokenObtainPairView,
    method='post',
    responses={status.HTTP_200_OK: TokenObtainPairResponseSerializer},
)

define_swagger_auto_schema(
    view=RegistrationAPIView,
    method='post',
    responses={status.HTTP_201_CREATED: UserSerializer}
)
