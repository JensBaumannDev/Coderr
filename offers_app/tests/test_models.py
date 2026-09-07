from django.test import TestCase
from django.contrib.auth import get_user_model
from offers_app.models import Offer, OfferDetail


class OfferModelTest(TestCase):
    def test_create_offer(self):
        testuser = get_user_model().objects.create_user(
            username="testuser", password="testpass123", type="business"
        )
        offer = Offer.objects.create(
            user=testuser, title="testtitle", description="testdescription"
        )
        self.assertEqual(offer.title, "testtitle")


class OfferDetailModelTest(TestCase):
    def test_create_offer_details(self):
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
        self.assertEqual(detail.price, 100)
