from django.contrib.auth import authenticate

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from core.serializers import SignupSerializer, LoginSerializer


class SignupView(APIView):
    """Register a new user and return JWT tokens upon successful creation."""

    def post(self, request):
        """Validate signup data, create the user, authenticate, and return access/refresh tokens."""
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        serializer.save()
        authenticated_user = authenticate(
            request, email=email, password=password
        )

        if authenticated_user:
            token = RefreshToken.for_user(authenticated_user)
            response = {
                "access": str(token.access_token),
                "refresh": str(token),
                "email": authenticated_user.email,
            }

            return Response(response, status=HTTP_201_CREATED)

        return Response({"errors": "Invalid email or password"}, status=HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
    """Authenticate a user with email/password and return JWT tokens."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Validate credentials, check active status, and return access/refresh tokens."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        authenticated_user = authenticate(
            request, email=serializer.validated_data["email"], password=serializer.validated_data["password"]
        )

        if not authenticated_user or not authenticated_user.is_active:
            return Response({"errors": "Invalid email or password"}, status=HTTP_401_UNAUTHORIZED)

        token = RefreshToken.for_user(authenticated_user)
        response = {
            "access": str(token.access_token),
            "refresh": str(token),
            "email": authenticated_user.email,
        }

        return Response(response, status=HTTP_200_OK)


class LogoutView(APIView):
    """Blacklist the provided refresh token to log the user out."""

    def post(self, request):
        """Accept a refresh token and blacklist it, invalidating the session."""
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"errors": ""})
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Logout successfully"},
                status=HTTP_200_OK,
            )
        except TokenError:
            return Response(
                {"error": "Invalid token"},
                status=HTTP_400_BAD_REQUEST,
            )
