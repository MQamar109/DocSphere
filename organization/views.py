from django.urls import reverse_lazy
from django.db.models import Q
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

    def get_queryset(self):
        queryset = Organization.objects.all()
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(slug__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '').strip()
        return context


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
    success_url = reverse_lazy('organization_list')


class OrganizationUpdateView(UpdateView):
    """Handle updating an existing organization."""

    model = Organization
    template_name = 'organization/organization_form.html'
    context_object_name = 'organization'
    fields = ['name', 'description']
    success_url = reverse_lazy('organization_list')


class OrganizationDeleteView(DeleteView):
    """Handle deletion of an organization with confirmation."""

    model = Organization
    template_name = 'organization/organization_confirm_delete.html'
    context_object_name = 'organization'
    success_url = reverse_lazy('organization_list')
