from django.test import TestCase
from .helpers import OrderTestMixin


class OrderModelTest(OrderTestMixin, TestCase):
    def setUp(self):
        self.customer = self.create_user("customer")
        self.business = self.create_user("business", "business")

    def test_order_is_created_with_in_progress_status(self):
        order = self.create_order(self.customer, self.business)
        self.assertEqual(order.status, "in_progress")
        self.assertEqual(order.customer_user, self.customer)
        self.assertEqual(order.business_user, self.business)

    def test_order_string_representation(self):
        order = self.create_order(self.customer, self.business)
        self.assertEqual(str(order), f"Order #{order.id}: Logo Paket")
