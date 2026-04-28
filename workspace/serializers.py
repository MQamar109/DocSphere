from rest_framework.serializers import ModelSerializer

from workspace.models import (
    Document,
    DocumentPermissions,
    Project,
    ProjectPermissions,
)


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class ProjectPermissionsSerializer(ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = ProjectPermissions
        fields = '__all__'


class DocumentPermissionsSerializer(ModelSerializer):
    document = DocumentSerializer()

    class Meta:
        model = DocumentPermissions
        fields = '__all__'
