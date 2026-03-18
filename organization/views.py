from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from organization.models import Organization


class OrganizationListView(ListView):
    """Display a list of all organizations."""

    model = Organization
    template_name = 'organization/organization_list.html'
    context_object_name = 'organizations'


class OrganizationDetailView(DetailView):
    """Display the details of a single organization."""

    model = Organization
    template_name = 'organization/organization_detail.html'
    context_object_name = 'organization'


class OrganizationCreateView(CreateView):
    """Handle creation of a new organization."""

    model = Organization
    template_name = 'organization/organization_form.html'
    context_object_name = 'organization'
    fields = ['name', 'description']
    success_url = reverse_lazy('organization-list')


class OrganizationUpdateView(UpdateView):
    """Handle updating an existing organization."""

    model = Organization
    template_name = 'organization/organization_form.html'
    context_object_name = 'organization'
    fields = ['name', 'description']
    success_url = reverse_lazy('organization-list')


class OrganizationDeleteView(DeleteView):
    """Handle deletion of an organization with confirmation."""

    model = Organization
    template_name = 'organization/organization_confirm_delete.html'
    context_object_name = 'organization'
    success_url = reverse_lazy('organization-list')
