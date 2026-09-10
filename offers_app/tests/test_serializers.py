from unittest.mock import Mock

from django.test import TestCase

from offers_app.api.serializers import (
    OfferCreateSerializer,
    OfferDetailSerializer,
    OfferSerializer,
)
from .helpers import OfferTestMixin


class OfferDetailSerializerTest(OfferTestMixin, TestCase):
    def test_offer_detail_serializer(self):
        detail = self.create_detail(self.create_offer(self.create_user()))
        serializer = OfferDetailSerializer(detail)
        self.assertEqual(serializer.data["price"], "100.00")


class OfferSerializerTest(OfferTestMixin, TestCase):
    def test_offer_serializer_min_values(self):
        offer = self.create_offer(self.create_user())
        self.create_detail(offer, price=100, delivery_time=7)
        self.create_detail(offer, price=50, delivery_time=3, offer_type="standard")
        serializer = OfferSerializer(offer)
        self.assertEqual(serializer.data["min_price"], "50.00")
        self.assertEqual(serializer.data["min_delivery_time"], 3)


class OfferCreateSerializerTest(OfferTestMixin, TestCase):
    def test_valid_offer_with_three_details(self):
        serializer = OfferCreateSerializer(data=self.offer_data())
        self.assertTrue(serializer.is_valid())

    def test_offer_with_two_details_invalid(self):
        serializer = OfferCreateSerializer(data=self.offer_data(2))
        self.assertFalse(serializer.is_valid())

    def test_create_offer_with_details(self):
        request = Mock(user=self.create_user("testuser"))
        serializer = OfferCreateSerializer(
            data=self.offer_data(), context={"request": request}
        )
        serializer.is_valid()
        offer = serializer.save()
        self.assertEqual(offer.details.count(), 3)
