from django.test import TestCase

from .helpers import OfferTestMixin


class OfferModelTest(OfferTestMixin, TestCase):
    def test_create_offer(self):
        offer = self.create_offer(self.create_user())
        self.assertEqual(offer.title, "testtitle")

    def test_offer_string_representation(self):
        offer = self.create_offer(self.create_user())
        self.assertEqual(str(offer), "testtitle")


class OfferDetailModelTest(OfferTestMixin, TestCase):
    def test_create_offer_details(self):
        detail = self.create_detail(self.create_offer(self.create_user()))
        self.assertEqual(detail.price, 100)

    def test_offer_detail_string_representation(self):
        detail = self.create_detail(self.create_offer(self.create_user()))
        self.assertEqual(str(detail), "testtitle (basic)")
