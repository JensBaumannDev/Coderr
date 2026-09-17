from rest_framework import serializers

from auth_app.models import User

from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializes a review."""
    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Validates and creates a new review."""
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(type="business")
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        """Checks that the customer has not reviewed this business user."""
        reviewer = self.context["request"].user
        review_exists = Review.objects.filter(
            business_user=attrs["business_user"],
            reviewer=reviewer,
        ).exists()
        if review_exists:
            raise serializers.ValidationError(
                "Eine Bewertung für diesen Business-User existiert bereits."
            )
        return attrs

    def create(self, validated_data):
        """Creates a review for the request user."""
        return Review.objects.create(
            reviewer=self.context["request"].user,
            **validated_data,
        )


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Updates the editable fields of a review."""
    class Meta:
        model = Review
        fields = ["rating", "description"]

    def validate(self, attrs):
        """Checks that only rating and description are changed."""
        invalid_fields = set(self.initial_data) - {"rating", "description"}
        if invalid_fields:
            raise serializers.ValidationError(
                "Nur rating und description dürfen geändert werden."
            )
        return attrs

    def to_representation(self, instance):
        """Returns the complete updated review."""
        return ReviewSerializer(instance).data
