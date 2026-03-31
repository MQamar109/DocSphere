from django.db.models import Count
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.models import User
from workspace.models import ProjectPermissions, DocumentPermissions
from organization.serializers import OrganizationSerializer
from workspace.serializers import (
    DocumentPermissionsSerializer,
    DocumentSerializer,
    ProjectPermissionsSerializer,
    ProjectSerializer,
)


class CreateUserSerializer(serializers.ModelSerializer):
    projects = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
    )
    documents = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'email', 'role', 'organization', 'projects',
            'documents', 'password', 'first_name', 'last_name',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        projects = validated_data.pop('projects', [])
        documents = validated_data.pop('documents', [])
        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password, **validated_data
        )

        if user.role == "user" and projects:
            raise ValidationError(
                "User cannot have projects"
            )

        if projects:
            for project in projects:
                ProjectPermissions.objects.create(
                    user=user,
                    project_id=project,
                    permissions="all",
                )

        if documents:
            for document in documents:
                DocumentPermissions.objects.create(
                    user=user,
                    document_id=document,
                    permissions=(
                        "all" if user.role == "user"
                        else "read"
                    ),
                )

        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    projects = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
    )
    documents = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'email', 'role', 'organization', 'projects',
            'documents', 'first_name', 'last_name',
        ]
        read_only_fields = ['email']

    def update(self, instance, validated_data):
        projects = validated_data.pop('projects', [])
        documents = validated_data.pop('documents', [])

        instance = super().update(instance, validated_data)

        if instance.role == "user" and projects:
            raise ValidationError(
                "User cannot have projects"
            )

        if projects:
            for project in projects:
                ProjectPermissions.objects.create(
                    user=instance,
                    project_id=project,
                    permissions="all",
                )

        if documents:
            for document in documents:
                DocumentPermissions.objects.create(
                    user=instance,
                    document_id=document,
                    permissions=(
                        "all" if instance.role == "user"
                        else "read"
                    ),
                )

        return instance


class ListDetailUserSerializer(serializers.ModelSerializer):
    projects = ProjectPermissionsSerializer(
        source='project_permissions', many=True, read_only=True
    )
    documents = DocumentPermissionsSerializer(
        source='document_permissions', many=True, read_only=True
    )
    project_count = serializers.SerializerMethodField()
    document_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'role', 'organization',
            'projects', 'documents', 'first_name', 'last_name',
            'project_count', 'document_count'
        ]

    def get_project_count(self, obj):
        return obj.project_permissions.count()

    def get_document_count(self, obj):
        return obj.document_permissions.count()

