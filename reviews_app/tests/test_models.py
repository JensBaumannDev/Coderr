from django.test import TestCase

from .helpers import ReviewTestMixin


class ReviewModelTest(ReviewTestMixin, TestCase):
    def setUp(self):
        self.customer = self.create_user("customer")
        self.business = self.create_user("business", "business")

    def test_review_is_created(self):
        review = self.create_review(self.business, self.customer)
        self.assertEqual(review.business_user, self.business)
        self.assertEqual(review.reviewer, self.customer)
        self.assertEqual(review.rating, 5)

    def test_review_string_representation(self):
        review = self.create_review(self.business, self.customer, 4)
        self.assertEqual(str(review), "Review 4 by customer")
