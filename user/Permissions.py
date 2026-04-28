from rest_framework.permissions import BasePermission


class IsAdminOrManager(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == "manager" or request.user.role == "admin")


class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
