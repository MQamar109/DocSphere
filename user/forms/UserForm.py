from django import forms

from organization.models import Organization
from user.choices import UserRole
from user.models import User
from workspace.models import Project, Document


class UserCreateForm(forms.ModelForm):
    """Used only for creating a user."""

    role = forms.ChoiceField(choices=UserRole.choices)

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

    role = forms.ChoiceField(choices=UserRole.choices)

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

        self.fields["projects"].queryset = Project.objects.all()
        self.fields["documents"].queryset = Document.objects.all()

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
   