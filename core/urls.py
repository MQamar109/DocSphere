from django.urls import path

from core.views import  CustomLoginView, CustomLogoutView


urlpatterns = [
    # HTML views    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]

