from django.test import TestCase
from rest_framework.test import APIRequestFactory
from orders_app.api.serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    OrderStatusSerializer,
)
from .helpers import OrderTestMixin


class OrderSerializerTest(OrderTestMixin, TestCase):
    def setUp(self):
        self.customer = self.create_user("customer")
        self.business = self.create_user("business", "business")

    def test_order_serializer_contains_required_fields(self):
        order = self.create_order(self.customer, self.business)
        serializer = OrderSerializer(order)
        self.assertEqual(serializer.data["customer_user"], self.customer.id)
        self.assertEqual(serializer.data["business_user"], self.business.id)
        self.assertEqual(serializer.data["status"], "in_progress")
        self.assertEqual(serializer.data["price"], "150.00")

    def test_create_serializer_creates_order_from_offer_detail(self):
        detail = self.create_offer_detail(self.business)
        request = APIRequestFactory().post("/api/orders/")
        request.user = self.customer
        serializer = OrderCreateSerializer(
            data={"offer_detail_id": detail.id},
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid())
        order = serializer.save()
        self.assertEqual(order.customer_user, self.customer)
        self.assertEqual(order.business_user, self.business)

    def test_status_serializer_updates_status(self):
        order = self.create_order(self.customer, self.business)
        serializer = OrderStatusSerializer(
            order,
            data={"status": "completed"},
            partial=True,
        )
        self.assertTrue(serializer.is_valid())
        updated_order = serializer.save()
        self.assertEqual(updated_order.status, "completed")

    def test_status_serializer_rejects_other_fields(self):
        serializer = OrderStatusSerializer(
            data={"status": "completed", "title": "Neuer Titel"}
        )
        self.assertFalse(serializer.is_valid())
