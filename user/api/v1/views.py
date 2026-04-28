# user/views.py

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

from user.Permissions import IsSuperAdmin, IsAdminOrManager
from user.models import User
from user.serializers import (
    CreateUserSerializer,
    ListDetailUserSerializer,
    UpdateUserSerializer,
)
from user.cache import (               
    get_cached_user,
    get_cached_user_list,
    invalidate_user_cache,
)


class UserListCreateAPIView(APIView):
    """List active users with optional search, or create a new user."""
    permission_classes = [IsAdminOrManager]

    def get(self, request):
        """Return active users in the current user's organization."""
        users = User.objects.prefetch_related(
            'project_permissions__project',
            'document_permissions__document'
            ).filter(
                is_active=True,
                organization=request.user.organization,
            )
        search = request.query_params.get("search")

        if search:
            users = User.objects.prefetch_related(
                'project_permissions__project',
                'document_permissions__document',
            ).filter(
                is_active=True
            ).filter(
                Q(email__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
            )
            serializer = ListDetailUserSerializer(users, many=True)
            return Response(serializer.data, status=HTTP_200_OK)

        data = get_cached_user_list()
        return Response(data, status=HTTP_200_OK)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            invalidate_user_cache(serializer.instance.id)
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateDeleteUserAPIView(APIView):
    permission_classes = [IsAdminOrManager]
    """Retrieve, partially update, or soft-delete a single user."""

    def get_object(self, pk):
        return get_object_or_404(
            User.objects.prefetch_related(
                'project_permissions__project',
                'document_permissions__document',
            ),
            pk=pk,
        )

    def get(self, request, pk):
        data = get_cached_user(pk)
        return Response(data, status=HTTP_200_OK)

    def patch(self, request, pk):
        user = self.get_object(pk)
        serializer = UpdateUserSerializer(
            user, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            invalidate_user_cache(pk)
            return Response(serializer.data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.is_active = False
        user.save()
        invalidate_user_cache(pk)
        return Response(status=HTTP_204_NO_CONTENT)


class CurrentUserDetailAPIView(APIView):
    """Return the profile of the currently authenticated user."""

    def get(self, request):
        """Return the current user's details, or 401 if unauthenticated."""
        user = request.user
        if user.is_authenticated:
            user = User.objects.prefetch_related(
                'project_permissions__project',
                'document_permissions__document',
            ).get(pk=user.id)
            serializer = ListDetailUserSerializer(user)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_401_UNAUTHORIZED)


class AllUsersAPIView(APIView):
    """Return all users across organizations."""

    permission_classes = [IsSuperAdmin]

    def get(self, request):
        users = User.objects.prefetch_related(
            'project_permissions__project',
            'document_permissions__document',
        ).all()
        serializer = ListDetailUserSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
