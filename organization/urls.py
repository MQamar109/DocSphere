from django.urls import path

from organization.api.v1.views import (
    list_create_organization,
    retrieve_partial_update_delete,
)
from organization.views import (
    OrganizationCreateView,
    OrganizationDeleteView,
    OrganizationDetailView,
    OrganizationListView,
    OrganizationUpdateView,
)

urlpatterns = [
    path(
        '',
        list_create_organization,
        name='organization-list-create',
    ),
    path(
        '<int:pk>/',
        retrieve_partial_update_delete,
        name='retrieve-partial-update-delete',
    ),
    path(
        'list/',
        OrganizationListView.as_view(),
        name='organization-list',
    ),
    path(
        'create/',
        OrganizationCreateView.as_view(),
        name='organization-create',
    ),
    path(
        'detail/<int:pk>/',
        OrganizationDetailView.as_view(),
        name='organization-detail',
    ),
    path(
        'update/<int:pk>/',
        OrganizationUpdateView.as_view(),
        name='organization-update',
    ),
    path(
        'delete/<int:pk>/',
        OrganizationDeleteView.as_view(),
        name='organization-delete',
    ),
]
