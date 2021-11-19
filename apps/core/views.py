from django.contrib.auth.mixins import LoginRequiredMixin


class BaseViewMixin(LoginRequiredMixin):
    pass
