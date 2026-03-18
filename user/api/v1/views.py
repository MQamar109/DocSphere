from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.views import APIView

from user.models import User
from user.serializers import (
    CreateUserSerializer,
    ListDetailUserSerializer,
    UpdateUserSerializer,
)


class ListCreateUserAPIView(APIView):
    def get(self, request):
        users = User.objects.prefetch_related(
            'project_permissions__project',
            'document_permissions__document'
            ).filter(is_active=True)
        search = request.query_params.get("search")

        if search:
            users = users.filter(
                Q(email__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
            )
        serializer = ListDetailUserSerializer(users, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=HTTP_400_BAD_REQUEST
        )


class RetrieveUpdateDeleteUserAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(
            User.objects.prefetch_related(
                'project_permissions__project',
                'document_permissions__document',
            ),
            pk=pk,
        )

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = ListDetailUserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)

    def patch(self, request, pk):
        user = self.get_object(pk)
        serializer = UpdateUserSerializer(
            user, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=HTTP_200_OK
            )

        return Response(
            data=serializer.errors, status=HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.is_active = False
        user.save()
        return Response(status=HTTP_204_NO_CONTENT)


class CurrentUserDetailAPIView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            user = User.objects.prefetch_related(
                'project_permissions__project',
                'document_permissions__document',
            ).get(pk=user.id)
            serializer = ListDetailUserSerializer(user)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_401_UNAUTHORIZED)