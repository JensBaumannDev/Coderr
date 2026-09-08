from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from offers_app.models import Offer, OfferDetail


class OfferListViewTest(APITestCase):
    def test_offer_list_success(self):
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
            delivery_time_in_days=5,
            price=100,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic",
        )
        response = self.client.get("/api/offers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
