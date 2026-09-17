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
            {"id": d.id, "url": f"/offerdetails/{d.id}/"} for d in obj.details.all()
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
        """Checks that a new offer has three packages."""
        if not self.partial and len(value) != 3:
            raise serializers.ValidationError("Ein Angebot benötigt genau 3 Details.")
        return value

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
