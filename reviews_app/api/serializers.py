from rest_framework import serializers
from auth_app.models import User
from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
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
        return Review.objects.create(
            reviewer=self.context["request"].user,
            **validated_data,
        )


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["rating", "description"]

    def validate(self, attrs):
        invalid_fields = set(self.initial_data) - {"rating", "description"}
        if invalid_fields:
            raise serializers.ValidationError(
                "Nur rating und description dürfen geändert werden."
            )
        return attrs

    def to_representation(self, instance):
        return ReviewSerializer(instance).data
