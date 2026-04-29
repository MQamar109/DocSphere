import stripe
from django.conf import settings
from django.contrib.auth import authenticate
from django.urls import reverse

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from core.serializers import LoginSerializer, SignupSerializer, StripeCheckoutSerializer, PasswordResetEmailSerializer, UpdatePasswordSerializer, SetResetPasswordSerializer
from core.email_service import send_email
from djstripe.models import Customer
from user.models import User


class SignupView(APIView):
    """Register a new user and return JWT tokens upon successful creation."""

    authentication_classes = []
    permission_classes = [AllowAny]

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

    authentication_classes = []
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

class SendResetPasswordEmailAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
        
    def post(self, request):
        serializer = PasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data["email"])
        if user and user.is_active:
            send_email(
                user.email,
                "Reset your DocSphere password",
                "Reset your DocSphere password here is the link: <a href=''>Reset your DocSphere password</a>",
                is_html=True,
            )
            return Response({"detail": "Reset password email sent successfully"}, status=HTTP_200_OK)
        
        return Response({"error": "User not found"}, status=HTTP_404_NOT_FOUND)
            


class UpdatePasswordAPIView(APIView):

    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"error": "Old password is incorrect"}, status=HTTP_400_BAD_REQUEST)

        if user.check_password(serializer.validated_data["new_password"]):
            return Response(
                {"error": "New password cannot be the same as your current password."},
                status=HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        token = RefreshToken.for_user(user)

        return Response(
            {              
                "access": str(token.access_token),
                "refresh": str(token),               
            },
            status=HTTP_200_OK,
        )


class SetResetPasswordAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
        
    def post(self, request):
        serializer = SetResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        token = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(token.access_token),
                "refresh": str(token),
            },
            status=HTTP_200_OK,
        )

        
class StripeCheckoutView(APIView):

    def post(self, request):
        stripe_secret_key = settings.STRIPE_TEST_SECRET_KEY
        if not stripe_secret_key:
            return Response(
                {"error": "Stripe secret key is not configured."},
                status=HTTP_400_BAD_REQUEST,
            )
        stripe.api_key = stripe_secret_key

        serializer = StripeCheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = serializer.validated_data["organization"]

        customer, created = Customer.get_or_create(subscriber=organization)

        session = stripe.checkout.Session.create(
            customer=customer.id,
            payment_method_types=["card"],
            line_items=[{
                "price": settings.STRIPE_PRO_PRICE_ID,
                "quantity": 1,
            }],
            mode="subscription",
            success_url=request.build_absolute_uri(reverse("stripe_success")),
            cancel_url=request.build_absolute_uri(reverse("stripe_cancel")),
        )

        return Response({'session_url': session.url}, status=HTTP_200_OK)
