from django.test import TestCase
from django.contrib.auth import get_user_model
from offers_app.models import Offer, OfferDetail
from offers_app.api.serializers import OfferSerializer, OfferDetailSerializer


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
