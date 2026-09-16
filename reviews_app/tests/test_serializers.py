from django.test import TestCase
from rest_framework.test import APIRequestFactory
from reviews_app.api.serializers import (
    ReviewCreateSerializer,
    ReviewSerializer,
    ReviewUpdateSerializer,
)
from .helpers import ReviewTestMixin


class ReviewSerializerTest(ReviewTestMixin, TestCase):
    def setUp(self):
        self.customer = self.create_user("customer")
        self.business = self.create_user("business", "business")

    def test_review_serializer_contains_required_fields(self):
        review = self.create_review(self.business, self.customer, 4)
        serializer = ReviewSerializer(review)
        self.assertEqual(serializer.data["business_user"], self.business.id)
        self.assertEqual(serializer.data["reviewer"], self.customer.id)
        self.assertEqual(serializer.data["rating"], 4)
        self.assertEqual(serializer.data["description"], "Sehr gute Arbeit")

    def test_create_serializer_sets_reviewer(self):
        request = APIRequestFactory().post("/api/reviews/")
        request.user = self.customer
        serializer = ReviewCreateSerializer(
            data={
                "business_user": self.business.id,
                "rating": 5,
                "description": "Tolle Zusammenarbeit",
            },
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid())
        review = serializer.save()
        self.assertEqual(review.reviewer, self.customer)

    def test_create_serializer_rejects_duplicate_review(self):
        self.create_review(self.business, self.customer)
        request = APIRequestFactory().post("/api/reviews/")
        request.user = self.customer
        serializer = ReviewCreateSerializer(
            data={
                "business_user": self.business.id,
                "rating": 5,
                "description": "Noch eine Bewertung",
            },
            context={"request": request},
        )
        self.assertFalse(serializer.is_valid())

    def test_update_serializer_rejects_other_fields(self):
        review = self.create_review(self.business, self.customer)
        serializer = ReviewUpdateSerializer(
            review,
            data={"rating": 4, "business_user": self.business.id},
            partial=True,
        )
        self.assertFalse(serializer.is_valid())
