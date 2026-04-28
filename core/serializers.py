from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from user.models import User
from organization.models import Organization


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise ValidationError("Password and confirm password are not equal")

        try:
            validate_password(attrs["password"])
        except DjangoValidationError as exc:
            raise ValidationError({"password": list(exc.messages)})

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user

    class Meta:
        model = User
        fields = ["email", "role", "password", "confirm_password"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        if attrs["new_password"] != attrs["confirm_password"]:
            raise ValidationError("New password and confirm password are not equal")
        
        try:
            validate_password(attrs["new_password"])
        except DjangoValidationError as exc:
            raise ValidationError({"new_password": list(exc.messages)})
                
        return attrs


class SetResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise ValidationError("New password and confirm password are not equal")
        
        try:
            validate_password(attrs["new_password"])
        except DjangoValidationError as exc:
            raise ValidationError({"new_password": list(exc.messages)})
        
        return attrs


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user or not user.is_active:
            raise ValidationError("User not found.")
        return value


class StripeCheckoutSerializer(serializers.Serializer):
    organization = serializers.IntegerField()

    def validate_organization(self, value):
        try:
            organization = Organization.objects.get(id=value)
        except Organization.DoesNotExist:
            raise ValidationError("Organization not found.")
        except Exception as e:
            raise ValidationError(str(e))

        if not organization.is_active:
            raise ValidationError("Organization is not active.")
        if organization.has_active_subscription():
            raise ValidationError("Organization already has an active subscription.")

        return organization