from rest_framework import status
from rest_framework.test import APITestCase
from auth_app.models import User
from offers_app.models import Offer
from reviews_app.models import Review


class BaseInfoViewTest(APITestCase):
    def setUp(self):
        self.business = self._create_user("business", "business")
        self.customer = self._create_user("customer")
        self.reviewer = self._create_user("reviewer")
        self._create_statistics()

    def _create_user(self, username, user_type="customer"):
        return User.objects.create_user(
            username=username,
            password="testpass123",
            type=user_type,
        )

    def _create_statistics(self):
        Offer.objects.create(user=self.business, title="Logo Design")
        self._create_review(self.customer, 4, "Sehr gute Arbeit")
        self._create_review(self.reviewer, 5, "Tolle Zusammenarbeit")

    def _create_review(self, reviewer, rating, description):
        Review.objects.create(
            business_user=self.business,
            reviewer=reviewer,
            rating=rating,
            description=description,
        )

    def test_base_info_returns_platform_statistics(self):
        response = self.client.get("/api/base-info/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["review_count"], 2)
        self.assertEqual(response.data["average_rating"], 4.5)
        self.assertEqual(response.data["business_profile_count"], 1)
        self.assertEqual(response.data["offer_count"], 1)


class EmptyBaseInfoViewTest(APITestCase):
    def test_base_info_returns_zero_for_empty_platform(self):
        response = self.client.get("/api/base-info/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["review_count"], 0)
        self.assertEqual(response.data["average_rating"], 0)
        self.assertEqual(response.data["business_profile_count"], 0)
        self.assertEqual(response.data["offer_count"], 0)
