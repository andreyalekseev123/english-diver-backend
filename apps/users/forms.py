from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class CustomAuthenticationForm(AuthenticationForm):
    """Custom AuthenticationForm for change error message."""

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password."
            " Note that password is case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }
