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

    def _offer_create_data(self):
        return {
            "title": "Grafikdesign-Paket",
            "description": "desc",
            "details": [
                {
                    "title": "Basic",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo", "Flyer"],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": ["Logo", "Flyer", "Card"],
                    "offer_type": "premium",
                },
            ],
        }

    def test_offer_create_success(self):
        business_user = get_user_model().objects.create_user(
            username="createbiz", password="testpass123", type="business"
        )
        self.client.force_authenticate(user=business_user)
        response = self.client.post(
            "/api/offers/", self._offer_create_data(), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_offer_create_forbidden_for_customer(self):
        customer_user = get_user_model().objects.create_user(
            username="createcust", password="testpass123", type="customer"
        )
        self.client.force_authenticate(user=customer_user)
        response = self.client.post(
            "/api/offers/", self._offer_create_data(), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_create_unauthenticated(self):
        response = self.client.post(
            "/api/offers/", self._offer_create_data(), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
