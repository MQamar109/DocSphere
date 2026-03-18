from django import forms

from organization.models import Organization
from user.models import User
from workspace.models import Project, Document

ROLE_CHOICES = [
    ('user', 'User'),
    ('manager', 'Manager'),
    ('admin', 'Admin'),
]


class UserCreateForm(forms.ModelForm):
    """Used only for creating a user."""

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all()
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "role",
            "organization",
            "password",
        ]
        widgets = {
            "password": forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Used for updating a user."""

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all()
    )

    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    documents = forms.ModelMultipleChoiceField(
        queryset=Document.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "role",
            "organization",
            "projects",
            "documents",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        role = self.data.get("role") or getattr(
            self.instance, "role", None
        )
        org_id = self.data.get("organization") or getattr(
            self.instance, "organization_id", None
        )

        if (
            hasattr(self.data, "getlist")
            and self.data.getlist("projects")
        ):
            project_ids = self.data.getlist("projects")
        else:
            project_ids = []

        if org_id:
            self.fields["projects"].queryset = (
                Project.objects.filter(organization_id=org_id)
            )
        else:
            self.fields["projects"].queryset = (
                Project.objects.all()
            )

        if role == "user":
            self.fields["documents"].queryset = (
                Document.objects.filter(project__isnull=True)
            )
        elif role in ["manager", "admin"]:
            if project_ids:
                self.fields["documents"].queryset = (
                    Document.objects.filter(
                        project_id__in=project_ids
                    )
                )
            else:
                self.fields["documents"].queryset = (
                    Document.objects.filter(
                        project__isnull=True
                    )
                )

        if self.instance and self.instance.pk:
            self.fields["projects"].initial = (
                Project.objects.filter(
                    projectpermissions__user=self.instance
                ).distinct()
            )

            self.fields["documents"].initial = (
                Document.objects.filter(
                    documentpermissions__user=self.instance
                ).distinct()
            )
