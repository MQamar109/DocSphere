from django.urls import path

from core.api.v1.views import LoginView, LogoutView, SignupView
from core.views import CustomLoginView, CustomLogoutView


urlpatterns = [
    # HTML views
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    # API auth views
    path('drf-login/', LoginView.as_view(), name='drf_login'),
    path('drf-logout/', LogoutView.as_view(), name='drf_logout'),
    path('drf-signup/', SignupView.as_view(), name='drf_signup'),
]

