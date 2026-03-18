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
    model = Organization
    template_name = 'organization/organization_list.html'
    context_object_name = 'organizations'


class OrganizationDetailView(DetailView):
    model = Organization
    template_name = 'organization/organization_detail.html'
    context_object_name = 'organization'


class OrganizationCreateView(CreateView):
    model = Organization
    template_name = 'organization/organization_form.html'
    context_object_name = 'organization'
    fields = ['name', 'description']
    success_url = reverse_lazy('organization-list')


class OrganizationUpdateView(UpdateView):
    model = Organization
    template_name = 'organization/organization_form.html'
    context_object_name = 'organization'
    fields = ['name', 'description']
    success_url = reverse_lazy('organization-list')


class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'organization/organization_confirm_delete.html'
    context_object_name = 'organization'
    success_url = reverse_lazy('organization-list')
