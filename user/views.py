from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from django.contrib.auth.mixins import LoginRequiredMixin

from organization.models import Organization
from user.forms.UserForm import UserCreateForm, UserUpdateForm
from user.models import User
from workspace.models import ProjectPermissions, DocumentPermissions


class UserListView(LoginRequiredMixin, ListView):
    """Display a list of all active users with their project and document counts."""

    model = User
    template_name = 'user/users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        """Return active users annotated with project and document counts."""
        return User.objects.filter(is_active=True).annotate(
            project_count=Count('projectpermissions'),
            document_count=Count('projectpermissions'),
        )


class UserDetailView(LoginRequiredMixin, DetailView):
    """Display a user's profile along with their project and document permissions."""

    model = User
    template_name = 'user/user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Enrich context with the user's project and document permissions."""
        context = super().get_context_data(**kwargs)
        context['projects'] = (
            ProjectPermissions.objects.filter(user=self.object)
        )
        context['documents'] = (
            DocumentPermissions.objects.filter(user=self.object)
        )
        return context


class UserCreateView(CreateView):
    """Handle creation of a new user account."""

    model = User
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('users-list')
    form_class = UserCreateForm


class UserUpdateView(UpdateView):
    """Handle updating user details and syncing project/document permissions."""

    model = User
    form_class = UserUpdateForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('users-list')

    def form_valid(self, form):
        """Save the user and create any newly assigned project/document permissions."""
        response = super().form_valid(form)

        user = self.object
        selected_projects = (
            form.cleaned_data.get("projects") or []
        )
        selected_documents = (
            form.cleaned_data.get("documents") or []
        )

        if selected_projects:
            for project in selected_projects:
                ProjectPermissions.objects.get_or_create(
                    user=user,
                    project=project,
                    defaults={"permissions": "all"},
                )

        if selected_documents:
            for document in selected_documents:
                DocumentPermissions.objects.get_or_create(
                    user=user,
                    document=document,
                    defaults={"permissions": "read"},
                )

        return response


class UserDeleteView(DeleteView):
    """Handle soft-deletion of a user by deactivating their account."""

    model = User
    template_name = 'user/user_delete_confirm.html'
    success_url = reverse_lazy('users-list')

    def delete(self, request, *args, **kwargs):
        """Soft-delete the user by setting is_active to False instead of removing the record."""
        user = self.get_object()
        user.is_active = False
        user.save()
        return redirect(self.success_url)
