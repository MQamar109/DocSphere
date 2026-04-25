from django.urls import path

from core.api.v1.views import (
    LoginView,
    LogoutView,
    UpdatePasswordAPIView,
    SetResetPasswordAPIView,
    SignupView,
    StripeCheckoutView,
    SendResetPasswordEmailAPIView,
)
from core.views import CustomLoginView, CustomLogoutView


urlpatterns = [
    # HTML views
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    # API auth views
    path('drf-login/', LoginView.as_view(), name='drf_login'),
    path('drf-logout/', LogoutView.as_view(), name='drf_logout'),
    path('drf-signup/', SignupView.as_view(), name='drf_signup'),
    path('drf-update-password/', UpdatePasswordAPIView.as_view(), name='drf_update_password'),
    path('drf-set-reset-password/', SetResetPasswordAPIView.as_view(), name='drf_set_reset_password'),
    path('drf-send-reset-password-email/', SendResetPasswordEmailAPIView.as_view(), name='drf_send_reset_password_email'),
    path('stripe-checkout/', StripeCheckoutView.as_view(), name='stripe_checkout'),
    
]

