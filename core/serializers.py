from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from user.models import User


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
