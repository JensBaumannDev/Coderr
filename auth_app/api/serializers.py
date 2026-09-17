from django.contrib.auth import authenticate
from rest_framework import serializers

from auth_app.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Validates and creates new user accounts."""
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password", "type"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        """Checks whether both passwords are identical."""
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        """Creates the user without the repeated password."""
        validated_data.pop("repeated_password")
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Validates login credentials."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Authenticates the user with the submitted credentials."""
        user = authenticate(
            username=attrs["username"], password=attrs["password"]
        )

        if user is None:
            raise serializers.ValidationError("Username or password not found")
        attrs["user"] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    """Serializes a complete user profile."""
    user = serializers.IntegerField(source="id", read_only=True)
    created_at = serializers.DateTimeField(
        source="date_joined", read_only=True
    )

    class Meta:
        model = User
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]
        extra_kwargs = {
            "username": {"read_only": True},
            "type": {"read_only": True},
        }


class ProfileListSerializer(serializers.ModelSerializer):
    """Serializes user profiles for profile lists."""
    user = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = User
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
        ]


class CustomerProfileListSerializer(serializers.ModelSerializer):
    """Serializes customer profiles for profile lists."""
    user = serializers.IntegerField(source="id", read_only=True)
    uploaded_at = serializers.DateTimeField(
        source="date_joined", read_only=True
    )

    class Meta:
        model = User
        fields = ["user", "username", "file", "uploaded_at", "type"]
