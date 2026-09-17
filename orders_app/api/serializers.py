from offers_app.models import OfferDetail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from ..models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serializes an order."""
    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]


class OrderCreateSerializer(serializers.Serializer):
    """Creates an order from an offer package."""
    offer_detail_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        """Creates an order with copied package data."""
        detail = validated_data["offer_detail_id"]
        order_data = self._order_data(detail)
        return Order.objects.create(
            customer_user=self.context["request"].user,
            business_user=detail.offer.user,
            **order_data,
        )

    def _order_data(self, detail):
        """Collects the package values for a new order."""
        fields = [
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]
        return {field: getattr(detail, field) for field in fields}

    def validate_offer_detail_id(self, value):
        """Returns the selected offer package or raises an error."""
        return get_object_or_404(OfferDetail, pk=value)

    def to_representation(self, instance):
        """Returns the complete created order."""
        return OrderSerializer(instance).data


class OrderStatusSerializer(serializers.ModelSerializer):
    """Updates only the status of an order."""
    class Meta:
        model = Order
        fields = ["status"]

    def validate(self, attrs):
        """Checks that only the status field is changed."""
        invalid_fields = set(self.initial_data) - {"status"}
        if invalid_fields:
            raise serializers.ValidationError(
                "Nur status darf geändert werden."
            )
        return attrs

    def to_representation(self, instance):
        """Returns the complete updated order."""
        return OrderSerializer(instance).data
