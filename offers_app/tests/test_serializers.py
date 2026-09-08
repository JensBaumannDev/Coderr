from unittest.mock import Mock
from django.test import TestCase
from django.contrib.auth import get_user_model
from offers_app.models import Offer, OfferDetail
from offers_app.api.serializers import (
    OfferSerializer,
    OfferDetailSerializer,
    OfferCreateSerializer,
)


class OfferDetailSerializerTest(TestCase):
    def test_offer_detail_serializer(self):
        testuser = get_user_model().objects.create_user(
            username="testuser", password="testpass123", type="business"
        )
        testoffer = Offer.objects.create(
            user=testuser, title="testtitle", description="testdescription"
        )
        detail = OfferDetail.objects.create(
            offer=testoffer,
            title="testtitle",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic",
        )
        serializer = OfferDetailSerializer(detail)
        self.assertEqual(serializer.data["price"], "100.00")


class OfferSerializerTest(TestCase):
    def test_offer_serializer_min_values(self):
        testuser = get_user_model().objects.create_user(
            username="testuser", password="testpass123", type="business"
        )
        testoffer = Offer.objects.create(
            user=testuser, title="testtitle", description="testdescription"
        )
        OfferDetail.objects.create(
            offer=testoffer,
            title="testtitle",
            revisions=2,
            delivery_time_in_days=7,
            price=100,
            features=[],
            offer_type="basic",
        )
        OfferDetail.objects.create(
            offer=testoffer,
            title="testtitle2",
            revisions=2,
            delivery_time_in_days=3,
            price=50,
            features=[],
            offer_type="standard",
        )
        serializer = OfferSerializer(testoffer)
        self.assertEqual(serializer.data["min_price"], "50.00")
        self.assertEqual(serializer.data["min_delivery_time"], 3)


class OfferCreateSerializerTest(TestCase):
    def test_valid_offer_with_three_details(self):
        testuser = get_user_model().objects.create_user(
            username="testuser", password="testpass123", type="business"
        )
        data = {
            "title": "Grafikdesign-Paket",
            "description": "Ein Angebot mit drei Paketen",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": ["Logo Design", "Visitenkarte", "Flyer"],
                    "offer_type": "premium",
                },
            ],
        }
        serializer = OfferCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_offer_with_two_details_invalid(self):
        data = {
            "title": "Grafikdesign-Paket",
            "description": "Ein Angebot mit drei Paketen",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "standard",
                },
            ],
        }
        serializer = OfferCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_create_offer_with_details(self):
        testuser = get_user_model().objects.create_user(
            username="testuser", password="testpass123", type="business"
        )
        request = Mock(user=testuser)
        data = {
            "title": "Grafikdesign-Paket",
            "description": "Ein Angebot mit drei Paketen",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": ["Logo Design", "Visitenkarte", "Flyer"],
                    "offer_type": "premium",
                },
            ],
        }
        serializer = OfferCreateSerializer(data=data, context={"request": request})
        serializer.is_valid()
        offer = serializer.save()
        self.assertEqual(offer.details.count(), 3)
