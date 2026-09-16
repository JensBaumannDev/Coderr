from rest_framework import status
from rest_framework.test import APITestCase
from .helpers import ReviewTestMixin


class ReviewListCreateViewTest(ReviewTestMixin, APITestCase):
    def setUp(self):
        self.customer = self.create_user("customer")
        self.other_customer = self.create_user("othercustomer")
        self.business = self.create_user("business", "business")
        self.other_business = self.create_user(
            "otherbusiness",
            "business",
        )

    def test_review_list_requires_authentication(self):
        response = self.client.get("/api/reviews/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_list_filters_by_business_user(self):
        review = self.create_review(self.business, self.customer)
        self.create_review(self.other_business, self.other_customer)
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(
            f"/api/reviews/?business_user_id={self.business.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], review.id)
        self.assertEqual(len(response.data), 1)

    def test_review_list_filters_by_reviewer(self):
        review = self.create_review(self.business, self.customer)
        self.create_review(self.other_business, self.other_customer)
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(
            f"/api/reviews/?reviewer_id={self.customer.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], review.id)
        self.assertEqual(len(response.data), 1)

    def test_review_list_orders_by_rating(self):
        self.create_review(self.business, self.customer, 5)
        self.create_review(self.business, self.other_customer, 2)
        self.client.force_authenticate(user=self.customer)
        response = self.client.get("/api/reviews/?ordering=rating")
        ratings = [review["rating"] for review in response.data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ratings, [2, 5])

    def test_customer_can_create_review(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.post(
            "/api/reviews/",
            {
                "business_user": self.business.id,
                "rating": 5,
                "description": "Tolle Zusammenarbeit",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["reviewer"], self.customer.id)
        self.assertEqual(response.data["business_user"], self.business.id)

    def test_business_user_cannot_create_review(self):
        self.client.force_authenticate(user=self.business)
        response = self.client.post(
            "/api/reviews/",
            {
                "business_user": self.other_business.id,
                "rating": 5,
                "description": "Nicht erlaubt",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_duplicate_review_returns_bad_request(self):
        self.create_review(self.business, self.customer)
        self.client.force_authenticate(user=self.customer)
        response = self.client.post(
            "/api/reviews/",
            {
                "business_user": self.business.id,
                "rating": 4,
                "description": "Doppelte Bewertung",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReviewDetailViewTest(ReviewTestMixin, APITestCase):
    def setUp(self):
        self.customer = self.create_user("customer")
        self.other_customer = self.create_user("othercustomer")
        self.business = self.create_user("business", "business")
        self.review = self.create_review(self.business, self.customer)

    def test_owner_can_update_review(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.patch(
            f"/api/reviews/{self.review.id}/",
            {"rating": 4, "description": "Aktualisierte Bewertung"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.review.id)
        self.assertEqual(response.data["rating"], 4)
        self.assertEqual(
            response.data["description"],
            "Aktualisierte Bewertung",
        )

    def test_other_customer_cannot_update_review(self):
        self.client.force_authenticate(user=self.other_customer)
        response = self.client.patch(
            f"/api/reviews/{self.review.id}/",
            {"rating": 4},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_update_rejects_other_fields(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.patch(
            f"/api/reviews/{self.review.id}/",
            {"rating": 4, "business_user": self.business.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_owner_can_delete_review(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.delete(f"/api/reviews/{self.review.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_other_customer_cannot_delete_review(self):
        self.client.force_authenticate(user=self.other_customer)
        response = self.client.delete(f"/api/reviews/{self.review.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_detail_returns_404_for_unknown_id(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.patch(
            "/api/reviews/9999/",
            {"rating": 4},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
