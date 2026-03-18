from django.urls import path

from user.views import (
    UserListView,
    UserDetailView,
    UserDeleteView,
    UserCreateView,
    UserUpdateView,
)

urlpatterns = [
    path('list/', UserListView.as_view(), name='users-list'),
    path('detail/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
   
]