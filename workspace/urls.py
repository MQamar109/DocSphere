from django.urls import path

from .views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    DocumentListView,
    DocumentDetailView,
    DocumentCreateView,
    DocumentUpdateView,
    DocumentDeleteView,
)
from workspace.api.v1.views import (
    ProjectListCreateAPIView,
    ProjectRetrieveUpdateDestroyAPIView,
    DocumentListCreateAPIView,
    DocumentRetrieveUpdateDestroyAPIView,
)


urlpatterns = [
    # Project URLs
    path("projects/", ProjectListView.as_view(), name="project_list"),
    path("projects/create/", ProjectCreateView.as_view(), name="project_create"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project_update"),
    path("projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"),

    # Document URLs
    path("documents/", DocumentListView.as_view(), name="document_list"),
    path("documents/create/", DocumentCreateView.as_view(), name="document_create"),
    path("documents/<int:pk>/", DocumentDetailView.as_view(), name="document_detail"),
    path("documents/<int:pk>/update/", DocumentUpdateView.as_view(), name="document_update"),
    path("documents/<int:pk>/delete/", DocumentDeleteView.as_view(), name="document_delete"),

    # DRF API URLs for both
    path("api/projects/", ProjectListCreateAPIView.as_view(), name="api_project_list_create"),
    path("api/projects/<int:pk>/", ProjectRetrieveUpdateDestroyAPIView.as_view(), name="api_project_detail"),
    path("api/documents/", DocumentListCreateAPIView.as_view(), name="api_document_list_create"),
    path("api/documents/<int:pk>/", DocumentRetrieveUpdateDestroyAPIView.as_view(), name="api_document_detail"),
]
