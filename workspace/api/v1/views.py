from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from workspace.models import Project, Document
from workspace.Permissions import UserDocumentPermission, UserProjectPermission
from workspace.serializers import ProjectSerializer, DocumentSerializer


class ProjectListCreateAPIView(ListCreateAPIView):
    """List all projects with search/filter support, or create a new project."""

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [UserProjectPermission]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['name']


class ProjectRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single project by its primary key."""

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [UserProjectPermission]


class DocumentListCreateAPIView(ListCreateAPIView):
    """List all documents with search/filter support, or create a new document."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['name']


class DocumentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single document by its primary key."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, UserDocumentPermission]
