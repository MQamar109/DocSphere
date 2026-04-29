from rest_framework.permissions import BasePermission
from workspace.models import ProjectPermissions, DocumentPermissions

class UserProjectPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["manager", "admin"]

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            return ProjectPermissions.objects.filter(
                user=request.user,
                project=obj,
                permissions__in=["all", "add"],
            ).exists()
        return True

class UserDocumentPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            if request.user.role == "manager":
                return ProjectPermissions.objects.filter(
                    user=request.user,
                    project=obj.project,
                    permissions__in=["all", "add"],
                ).exists()
            return DocumentPermissions.objects.filter(
                user=request.user,
                document=obj,
                permissions__in=["all", "write"],
            ).exists()
        return True