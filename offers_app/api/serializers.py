from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """Serializes one offer package."""
    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferSerializer(serializers.ModelSerializer):
    """Serializes an offer with calculated display values."""
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    def get_details(self, obj):
        """Returns links for all offer packages."""
        return [
            {"id": detail.id, "url": f"/offerdetails/{detail.id}/"}
            for detail in obj.details.all()
        ]

    def get_min_price(self, obj):
        """Returns the lowest package price."""
        return str(min(d.price for d in obj.details.all()))

    def get_min_delivery_time(self, obj):
        """Returns the shortest package delivery time."""
        return min(d.delivery_time_in_days for d in obj.details.all())

    def get_user_details(self, obj):
        """Returns public details of the offer owner."""
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username,
        }

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]


class OfferCreateSerializer(serializers.ModelSerializer):
    """Validates and saves offers with their packages."""
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]

    def validate_details(self, value):
        """Checks offer package types and delivery times."""
        self._validate_delivery_times(value)
        if not self.partial:
            self._validate_package_types(value)
        return value

    def _validate_delivery_times(self, details):
        """Checks that supplied delivery times are greater than zero."""
        for detail in details:
            delivery_time = detail.get("delivery_time_in_days")
            if delivery_time is not None and delivery_time <= 0:
                raise serializers.ValidationError(
                    "Delivery time must be greater than zero."
                )

    def _validate_package_types(self, details):
        """Checks that a new offer contains the required package types."""
        package_types = {detail["offer_type"] for detail in details}
        required_types = {"basic", "standard", "premium"}
        if len(details) != 3 or package_types != required_types:
            raise serializers.ValidationError(
                "An offer needs basic, standard, and premium packages."
            )

    def create(self, validated_data):
        """Creates an offer and all submitted packages."""
        details_data = validated_data.pop("details")
        offer = Offer.objects.create(
            user=self.context["request"].user, **validated_data
        )
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer

    def update(self, instance, validated_data):
        """Updates an offer and its existing packages."""
        details_data = validated_data.pop("details", [])
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        for detail in details_data:
            existing = instance.details.get(offer_type=detail["offer_type"])
            for key, value in detail.items():
                setattr(existing, key, value)
            existing.save()
        return instance
