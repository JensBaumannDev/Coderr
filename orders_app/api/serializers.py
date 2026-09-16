from offers_app.models import OfferDetail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from ..models import Order


class OrderSerializer(serializers.ModelSerializer):
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
    offer_detail_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        detail = validated_data["offer_detail_id"]
        order_data = self._order_data(detail)
        return Order.objects.create(
            customer_user=self.context["request"].user,
            business_user=detail.offer.user,
            **order_data,
        )

    def _order_data(self, detail):
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
        return get_object_or_404(OfferDetail, pk=value)

    def to_representation(self, instance):
        return OrderSerializer(instance).data


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]

    def validate(self, attrs):
        invalid_fields = set(self.initial_data) - {"status"}
        if invalid_fields:
            raise serializers.ValidationError(
                "Nur status darf geändert werden."
            )
        return attrs

    def to_representation(self, instance):
        return OrderSerializer(instance).data
