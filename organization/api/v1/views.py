from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from organization.models import Organization
from organization.serializers import OrganizationSerializer


@api_view(["GET", "POST"])
def list_create_organization(request):
    if request.method == "GET":
        organizations = Organization.objects.all()
        search = request.query_params.get("search")
        status = request.query_params.get("status")

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
            return Response(
                data=serializer.data, status=HTTP_201_CREATED
            )

        return Response(
            data=serializer.errors, status=HTTP_400_BAD_REQUEST
        )


@api_view(["GET", "PATCH", "DELETE"])
def retrieve_partial_update_delete(request, pk):
    try:
        instance = Organization.objects.get(id=pk)
    except Organization.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = OrganizationSerializer(instance)
        return Response(
            data=serializer.data, status=HTTP_200_OK
        )

    elif request.method == "PATCH":
        serializer = OrganizationSerializer(
            instance, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data, status=HTTP_200_OK
            )

        return Response(
            data=serializer.errors, status=HTTP_400_BAD_REQUEST
        )

    elif request.method == "DELETE":
        instance.delete()
        instance.save()
        return Response(status=HTTP_204_NO_CONTENT)
