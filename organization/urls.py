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
        name='organization_list_create',
    ),
    path(
        '<int:pk>/',
        retrieve_partial_update_delete,
        name='organization_retrieve_partial_update_delete',
    ),
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
