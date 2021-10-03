from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import PasswordResetForm
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from django_object_actions import DjangoObjectActions
from imagekit.admin import AdminThumbnail

from apps.users.models import User


def require_change_permissions(func):
    """Decorator that add checking of permissions for admin object actions

    It should be applied to sesetive admin object actions, like

        class UserAdmin(admin.ModelAdmin):
            change_actions = ["deactivate"]

            @require_change_permission
            def deactivate(self, request, obj):
                pass
    """

    def _wrapped(self, request, obj):
        if not self.has_change_permission(request, obj):
            return None
        return func(self, request, obj)

    return _wrapped


class CustomUserCreateForm(ModelForm):
    """Custom form for user creation in admin."""

    class Meta:
        model = User
        fields = "__all__"  # fields list limited in admin fieldset


@admin.register(User)
class UserAdmin(DjangoObjectActions, DjangoUserAdmin):
    """UI for User model."""
    add_form = CustomUserCreateForm
    ordering = ("email",)
    avatar_thumbnail = AdminThumbnail(image_field="avatar_thumbnail")
    list_display = (
        "avatar_thumbnail",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
    )
    list_display_links = (
        "email",
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name"),
        }),
        (_("Permissions"), {
            "classes": ("wide",),
            "fields": ("is_staff", "is_superuser", ),
        }),
    )
    fieldsets = (
        (None, {
            "fields": (
                "email",
                "password"
            )
        }),
        (_("Personal info"), {
            "fields": (
                "first_name",
                "last_name",
                "avatar",
            )
        }),
        (_("Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions"
            )
        }),
        (_("Important dates"), {
            "fields": (
                "created",
                "modified"
            )
        }),
    )
    readonly_fields = DjangoUserAdmin.readonly_fields + (
        "created",
        "modified",
    )
    change_actions = [
        "send_password_reset_email",
    ]

    @require_change_permissions
    def send_password_reset_email(self, request, obj):
        """Action to send password reset email to user.

        Method uses ``PasswordResetForm`` to send email.

        """
        form = PasswordResetForm(data={"email": obj.email})

        if not form.is_valid():
            # pylint:disable=invalid-string-quote
            msg = 'Email was not sent to "{}"'.format(obj.email)
            self.message_user(request, msg, messages.ERROR)

        form.save(request=request)

        # pylint:disable=invalid-string-quote
        msg = 'Email was successfully sent to "{}"'.format(obj.email)
        return self.message_user(request, msg, messages.SUCCESS)

    def get_changeform_initial_data(self, request):
        """Set default values for user creation in admin"""
        return {"is_staff": True, "is_superuser": True}
