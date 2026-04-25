from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class CustomLoginView(LoginView):
    """Handle user authentication and login."""

    template_name = 'registration/login.html'
    success_url = reverse_lazy('users_list')


class CustomLogoutView(LogoutView):
    """Handle user logout and session termination."""

    template_name = 'registration/logout.html'


class StripeSuccessView(TemplateView):
    """Render page shown after successful Stripe checkout."""

    template_name = "core/stripe_success.html"


class StripeCancelView(TemplateView):
    """Render page shown when Stripe checkout is cancelled."""

    template_name = "core/stripe_cancel.html"
