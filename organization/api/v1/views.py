from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from organization.cache import (
    get_cached_organization,
    get_cached_organization_list,
    invalidate_organization_cache,
)
from organization.models import Organization
from organization.permissions import IsSuperAdmin
from organization.serializers import OrganizationSerializer


@api_view(["GET", "POST"])
@permission_classes([IsSuperAdmin])
def list_create_organization(request):
    """List organizations with optional search/status filtering, or create a new one."""
    if request.method == "GET":
        search = request.query_params.get("search")
        status = request.query_params.get("status")

        # Serve cached data only for the active list endpoint shape.
        if not search and status == "active":
            data = get_cached_organization_list()
            return Response(data, status=HTTP_200_OK)

        organizations = Organization.objects.all()

        if search:
            organizations = organizations.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
            )

        if status:
            organizations = organizations.filter(
                is_active=(status == "active")
            )
        serializer = OrganizationSerializer(
            organizations, many=True
        )

        return Response(serializer.data, status=HTTP_200_OK)

    elif request.method == "POST":
        serializer = OrganizationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            invalidate_organization_cache(serializer.instance.id)
            return Response(
                data=serializer.data, status=HTTP_201_CREATED
            )

        return Response(
            data=serializer.errors, status=HTTP_400_BAD_REQUEST
        )


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsSuperAdmin])
def retrieve_partial_update_delete(request, pk):
    """Retrieve, partially update, or delete a single organization by pk."""
    try:
        instance = Organization.objects.get(id=pk)
    except Organization.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    if request.method == "GET":
        data = get_cached_organization(pk)
        return Response(data=data, status=HTTP_200_OK)

    elif request.method == "PATCH":
        serializer = OrganizationSerializer(
            instance, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            invalidate_organization_cache(instance.id)
            return Response(
                data=serializer.data, status=HTTP_200_OK
            )

        return Response(
            data=serializer.errors, status=HTTP_400_BAD_REQUEST
        )

    elif request.method == "DELETE":
        invalidate_organization_cache(instance.id)
        instance.delete()
        return Response(status=HTTP_204_NO_CONTENT)
