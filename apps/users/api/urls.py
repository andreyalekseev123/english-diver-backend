from django.urls import path

from rest_framework_simplejwt import views as jwt_views

from .schema import *
from .views import (
    PasswordResetConfirmView,
    PasswordResetView,
    RegistrationAPIView,
    UserInfoView,
)

app_name = "users_api"
urlpatterns = [
    path("registration/", RegistrationAPIView.as_view()),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "password/reset/",
        PasswordResetView.as_view(),
        name="rest_password_reset",
    ),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
    path("user-info/", UserInfoView.as_view())
]