from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect


class AdminRequeridoMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Sin sesión -> login. Con sesión pero sin ser admin -> home."""

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()