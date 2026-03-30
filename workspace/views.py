from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Project, Document


class ProjectListView(ListView):
    """Display a list of all projects."""

    model = Project
    template_name = "project/project_list.html"
    context_object_name = "projects"


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
