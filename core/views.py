from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('users-list')


class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'
