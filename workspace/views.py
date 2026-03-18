from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Project, Document


class ProjectListView(ListView):
    model = Project
    template_name = "project/project_list.html"
    context_object_name = "projects"


class ProjectDetailView(DetailView):
    model = Project
    template_name = "project/project_detail.html"
    context_object_name = "project"


class ProjectCreateView(CreateView):
    model = Project
    template_name = "project/project_form.html"
    context_object_name = "project"
    fields = ["name", "description", "organization"]
    success_url = reverse_lazy("project-list")


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = "project/project_form.html"
    context_object_name = "project"
    fields = ["name", "description", "organization"]
    success_url = reverse_lazy("project-list")


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "project/project_confirm_delete.html"
    context_object_name = "project"
    success_url = reverse_lazy("project-list")


class DocumentListView(ListView):
    model = Document
    template_name = "document/document_list.html"
    context_object_name = "documents"


class DocumentDetailView(DetailView):
    model = Document
    template_name = "document/document_detail.html"
    context_object_name = "document"


class DocumentCreateView(CreateView):
    model = Document
    template_name = "document/document_form.html"
    context_object_name = "document"
    fields = ["name", "description", "project"]
    success_url = reverse_lazy("document-list")


class DocumentUpdateView(UpdateView):
    model = Document
    template_name = "document/document_form.html"
    context_object_name = "document"
    fields = ["name", "description", "project"]
    success_url = reverse_lazy("document-list")


class DocumentDeleteView(DeleteView):
    model = Document
    template_name = "document/document_confirm_delete.html"
    context_object_name = "document"
    success_url = reverse_lazy("document-list")
