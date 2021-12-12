from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username"]


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            "email": {
                "error_messages": {
                    "required": "Give your email",
                },
            }
        }

    def validate(self, attrs):
        password = attrs.get("password")
        errors = dict()
        try:
            password_validation.validate_password(password, self.instance)
        except ValidationError as error:
            errors["password"] = error.messages

        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects._create_user(**validated_data)


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(
            data=self.initial_data
        )

        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_("Error"))

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                _("There aren't user with this email")
            )

        return value

    def save(self):
        request = self.context.get("request")
        # Set some values to trigger the send_email method.
        opts = {
            "use_https": not settings.DEBUG,
            "from_email": getattr(settings, "DEFAULT_FROM_EMAIL"),
            "request": request,
            "email_template_name": "account/password_reset_email.html",
            "html_email_template_name": "account/password_reset_email.html",
            "domain_override": settings.FRONTEND_DOMAIN,
        }
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    new_password1 = serializers.CharField(
        min_length=8,
        max_length=128,
    )
    new_password2 = serializers.CharField(
        min_length=8,
        max_length=128,
    )

    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    set_password_form_class = SetPasswordForm

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs["uid"]))
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"uid": ["Invalid value"]})

        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs["token"]):
            raise serializers.ValidationError({"token": ["Invalid value"]})

        return attrs

    def save(self):
        self.set_password_form.save()
