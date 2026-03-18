from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    """Handle user authentication and login."""

    template_name = 'registration/login.html'
    success_url = reverse_lazy('users-list')


class CustomLogoutView(LogoutView):
    """Handle user logout and session termination."""

    template_name = 'registration/logout.html'
