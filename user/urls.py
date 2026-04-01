from django.urls import path

from user.api.v1.views import ListCreateUserAPIView, RetrieveUpdateDeleteUserAPIView, CurrentUserDetailAPIView
from user.views import (
    UserListView,
    UserDetailView,
    UserDeleteView,
    UserCreateView,
    UserUpdateView,
)


urlpatterns = [
    path('list/', UserListView.as_view(), name='users_list'),
    path('detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('', ListCreateUserAPIView.as_view(), name='user_list_create_api'),
    path('<int:pk>/', RetrieveUpdateDeleteUserAPIView.as_view(), name='user_retrieve_update_delete_api'),
    path('me/', CurrentUserDetailAPIView.as_view(), name='user_me'),
   
]
