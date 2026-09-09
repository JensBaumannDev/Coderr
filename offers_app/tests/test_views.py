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


class OfferDetailRetrieveViewTest(APITestCase):
    def test_offerdetail_retrieve_success(self):
        customer_user = get_user_model().objects.create_user(
            username="createcust", password="testpass123", type="customer"
        )
        testoffer = Offer.objects.create(
            user=customer_user, title="testtitle", description="testdescription"
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
        self.client.force_authenticate(user=customer_user)
        response = self.client.get(f"/api/offerdetails/{detail.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OfferDetailViewTest(APITestCase):
    def _create_offer_with_details(self, owner):
        offer = Offer.objects.create(user=owner, title="testtitle", description="desc")
        OfferDetail.objects.create(
            offer=offer,
            title="Basic",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=[],
            offer_type="basic",
        )
        OfferDetail.objects.create(
            offer=offer,
            title="Standard",
            revisions=5,
            delivery_time_in_days=7,
            price=200,
            features=[],
            offer_type="standard",
        )
        OfferDetail.objects.create(
            offer=offer,
            title="Premium",
            revisions=10,
            delivery_time_in_days=10,
            price=500,
            features=[],
            offer_type="premium",
        )
        return offer

    def test_offer_retrieve_success(self):
        owner = get_user_model().objects.create_user(
            username="retrieveowner", password="testpass123", type="business"
        )
        offer = self._create_offer_with_details(owner)
        self.client.force_authenticate(user=owner)
        response = self.client.get(f"/api/offers/{offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_offer_retrieve_unauthenticated(self):
        owner = get_user_model().objects.create_user(
            username="retrieveowner2", password="testpass123", type="business"
        )
        offer = self._create_offer_with_details(owner)
        response = self.client.get(f"/api/offers/{offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_patch_owner_success(self):
        owner = get_user_model().objects.create_user(
            username="patchowner", password="testpass123", type="business"
        )
        offer = self._create_offer_with_details(owner)
        self.client.force_authenticate(user=owner)
        response = self.client.patch(
            f"/api/offers/{offer.id}/",
            {"title": "Updated", "details": [{"offer_type": "basic", "price": 150}]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_offer_patch_forbidden_for_non_owner(self):
        owner = get_user_model().objects.create_user(
            username="patchowner2", password="testpass123", type="business"
        )
        other_user = get_user_model().objects.create_user(
            username="patchother2", password="testpass123", type="business"
        )
        offer = self._create_offer_with_details(owner)
        self.client.force_authenticate(user=other_user)
        response = self.client.patch(
            f"/api/offers/{offer.id}/", {"title": "Hacked"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_delete_owner_success(self):
        owner = get_user_model().objects.create_user(
            username="deleteowner", password="testpass123", type="business"
        )
        offer = self._create_offer_with_details(owner)
        self.client.force_authenticate(user=owner)
        response = self.client.delete(f"/api/offers/{offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_offer_delete_forbidden_for_non_owner(self):
        owner = get_user_model().objects.create_user(
            username="deleteowner2", password="testpass123", type="business"
        )
        other_user = get_user_model().objects.create_user(
            username="deleteother2", password="testpass123", type="business"
        )
        offer = self._create_offer_with_details(owner)
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(f"/api/offers/{offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_patch_unauthenticated(self):
        owner = get_user_model().objects.create_user(
            username="patchowner3", password="testpass123", type="business"
        )
        offer = self._create_offer_with_details(owner)
        response = self.client.patch(
            f"/api/offers/{offer.id}/", {"title": "Hacked"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_delete_unauthenticated(self):
        owner = get_user_model().objects.create_user(
            username="deleteowner3", password="testpass123", type="business"
        )
        offer = self._create_offer_with_details(owner)
        response = self.client.delete(f"/api/offers/{offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
