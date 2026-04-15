from django.urls import path

from organization.views import (
    OrganizationCreateView,
    OrganizationDeleteView,
    OrganizationDetailView,
    OrganizationListView,
    OrganizationUpdateView,
)


urlpatterns = [
    path(
        'list/',
        OrganizationListView.as_view(),
        name='organization_list',
    ),
    path(
        'create/',
        OrganizationCreateView.as_view(),
        name='organization_create',
    ),
    path(
        'detail/<int:pk>/',
        OrganizationDetailView.as_view(),
        name='organization_detail',
    ),
    path(
        'update/<int:pk>/',
        OrganizationUpdateView.as_view(),
        name='organization_update',
    ),
    path(
        'delete/<int:pk>/',
        OrganizationDeleteView.as_view(),
        name='organization_delete',
    ),
]
