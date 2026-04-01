from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Project, Document


class ProjectListView(ListView):
    """Display a list of all projects."""

    model = Project
    template_name = "project/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        queryset = Project.objects.select_related("organization")
        search_query = self.request.GET.get("q", "").strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(organization__name__icontains=search_query)
            )
        return queryset.order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class ProjectDetailView(DetailView):
    """Display the details of a single project."""

    model = Project
    template_name = "project/project_detail.html"
    context_object_name = "project"


class ProjectCreateView(CreateView):
    """Handle creation of a new project."""

    model = Project
    template_name = "project/project_form.html"
    context_object_name = "project"
    fields = ["name", "description", "organization"]
    success_url = reverse_lazy("project_list")


class ProjectUpdateView(UpdateView):
    """Handle updating an existing project."""

    model = Project
    template_name = "project/project_form.html"
    context_object_name = "project"
    fields = ["name", "description", "organization"]
    success_url = reverse_lazy("project_list")


class ProjectDeleteView(DeleteView):
    """Handle deletion of a project with confirmation."""

    model = Project
    template_name = "project/project_confirm_delete.html"
    context_object_name = "project"
    success_url = reverse_lazy("project_list")


class DocumentListView(ListView):
    """Display a list of all documents."""

    model = Document
    template_name = "document/document_list.html"
    context_object_name = "documents"

    def get_queryset(self):
        queryset = Document.objects.select_related("project")
        search_query = self.request.GET.get("q", "").strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(project__name__icontains=search_query)
            )
        return queryset.order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class DocumentDetailView(DetailView):
    """Display the details of a single document."""

    model = Document
    template_name = "document/document_detail.html"
    context_object_name = "document"


class DocumentCreateView(CreateView):
    """Handle creation of a new document."""

    model = Document
    template_name = "document/document_form.html"
    context_object_name = "document"
    fields = ["name", "description", "project"]
    success_url = reverse_lazy("document_list")


class DocumentUpdateView(UpdateView):
    """Handle updating an existing document."""

    model = Document
    template_name = "document/document_form.html"
    context_object_name = "document"
    fields = ["name", "description", "project"]
    success_url = reverse_lazy("document_list")


class DocumentDeleteView(DeleteView):
    """Handle deletion of a document with confirmation."""

    model = Document
    template_name = "document/document_confirm_delete.html"
    context_object_name = "document"
    success_url = reverse_lazy("document_list")
