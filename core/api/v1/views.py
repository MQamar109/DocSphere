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
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            authenticated_user = authenticate(
                request, email=email, password=password
            )
            token = RefreshToken.for_user(authenticated_user)
            response = {
                "access": str(token.access_token),
                "refresh": str(token),
                "email": authenticated_user.email,
            }

            return Response(response, status=HTTP_201_CREATED)

        return Response(
            data=serializer.errors, status=HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            authenticated_user = authenticate(
                request, email=email, password=password
            )

            if not authenticated_user:
                return Response(
                    {"errors": "Invalid email or password"},
                    status=HTTP_401_UNAUTHORIZED,
                )

            if not authenticated_user.is_active:
                return Response(
                    {"errors": "User is not active"},
                    status=HTTP_403_FORBIDDEN,
                )

            token = RefreshToken.for_user(authenticated_user)
            response = {
                "access": str(token.access_token),
                "refresh": str(token),
                "email": authenticated_user.email,
            }

            return Response(response, status=HTTP_200_OK)

        return Response(
            data=serializer.errors, status=HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    def post(self, request):
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
