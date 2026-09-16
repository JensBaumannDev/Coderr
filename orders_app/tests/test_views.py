from rest_framework import status
from rest_framework.test import APITestCase
from .helpers import OrderTestMixin


class OrderListCreateViewTest(OrderTestMixin, APITestCase):
    def setUp(self):
        self.customer = self.create_user("customer")
        self.other_customer = self.create_user("othercustomer")
        self.business = self.create_user("business", "business")

    def test_order_list_returns_only_own_orders(self):
        own_order = self.create_order(self.customer, self.business)
        self.create_order(self.other_customer, self.business)
        self.client.force_authenticate(user=self.customer)
        response = self.client.get("/api/orders/")
        order_ids = [order["id"] for order in response.data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_ids, [own_order.id])

    def test_order_list_requires_authentication(self):
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_can_create_order(self):
        detail = self.create_offer_detail(self.business)
        self.client.force_authenticate(user=self.customer)
        response = self.client.post(
            "/api/orders/",
            {"offer_detail_id": detail.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["customer_user"], self.customer.id)
        self.assertEqual(response.data["business_user"], self.business.id)
        self.assertEqual(response.data["status"], "in_progress")

    def test_order_creation_returns_404_for_missing_detail(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.post(
            "/api/orders/",
            {"offer_detail_id": 9999},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_business_user_cannot_create_order(self):
        detail = self.create_offer_detail(self.business)
        self.client.force_authenticate(user=self.business)
        response = self.client.post(
            "/api/orders/",
            {"offer_detail_id": detail.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrderDetailViewTest(OrderTestMixin, APITestCase):
    def setUp(self):
        self.customer = self.create_user("customer")
        self.business = self.create_user("business", "business")
        self.other_business = self.create_user("otherbusiness", "business")
        self.order = self.create_order(self.customer, self.business)

    def test_business_user_can_update_own_order_status(self):
        self.client.force_authenticate(user=self.business)
        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {"status": "completed"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.order.id)
        self.assertEqual(response.data["title"], self.order.title)
        self.assertEqual(response.data["status"], "completed")

    def test_other_business_user_cannot_update_order(self):
        self.client.force_authenticate(user=self.other_business)
        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {"status": "completed"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_cannot_update_order_status(self):
        invalid_order = self.create_order(self.customer, self.customer)
        self.client.force_authenticate(user=self.customer)
        response = self.client.patch(
            f"/api/orders/{invalid_order.id}/",
            {"status": "completed"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_status_rejects_other_fields(self):
        self.client.force_authenticate(user=self.business)
        response = self.client.patch(
            f"/api/orders/{self.order.id}/",
            {"status": "completed", "title": "Neuer Titel"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_staff_user_can_delete_order(self):
        staff_user = self.create_user("staff", "business")
        staff_user.is_staff = True
        staff_user.save()
        self.client.force_authenticate(user=staff_user)
        response = self.client.delete(f"/api/orders/{self.order.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_staff_user_cannot_delete_order(self):
        self.client.force_authenticate(user=self.business)
        response = self.client.delete(f"/api/orders/{self.order.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrderCountViewTest(OrderTestMixin, APITestCase):
    def setUp(self):
        self.customer = self.create_user("customer")
        self.business = self.create_user("business", "business")
        self.create_order(self.customer, self.business, "in_progress")
        self.create_order(self.customer, self.business, "completed")
        self.create_order(self.customer, self.business, "cancelled")

    def test_in_progress_order_count(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(f"/api/order-count/{self.business.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order_count"], 1)

    def test_completed_order_count(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(
            f"/api/completed-order-count/{self.business.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed_order_count"], 1)

    def test_order_count_requires_authentication(self):
        response = self.client.get(f"/api/order-count/{self.business.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_count_returns_404_for_customer_id(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(f"/api/order-count/{self.customer.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
