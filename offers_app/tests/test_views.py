from rest_framework import status
from rest_framework.test import APITestCase

from .helpers import OfferTestMixin


class OfferListViewTest(OfferTestMixin, APITestCase):
    def assert_offer_results(self, response, *offers):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), len(offers))
        returned_ids = [item["id"] for item in response.data["results"]]
        self.assertEqual(returned_ids, [offer.id for offer in offers])

    def _offer_create_data(self):
        return self.offer_data()

    def test_offer_list_success(self):
        self.create_listing_offer(self.create_user("testuser"), "testtitle")
        response = self.client.get("/api/offers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_offer_create_success(self):
        self.client.force_authenticate(user=self.create_user("createbiz"))
        response = self.client.post(
            "/api/offers/", self._offer_create_data(), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_offer_create_forbidden_for_customer(self):
        user = self.create_user("createcust", "customer")
        self.client.force_authenticate(user=user)
        response = self.client.post(
            "/api/offers/", self._offer_create_data(), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_create_unauthenticated(self):
        response = self.client.post(
            "/api/offers/", self._offer_create_data(), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_list_filter_by_creator_id(self):
        first_user = self.create_user("business1")
        first_offer = self.create_listing_offer(first_user, "first")
        self.create_listing_offer(self.create_user("business2"), "second")
        response = self.client.get(f"/api/offers/?creator_id={first_user.id}")
        self.assert_offer_results(response, first_offer)

    def test_offer_list_filter_by_min_price(self):
        user = self.create_user()
        cheap_offer = self.create_listing_offer(user, "cheap", price=50)
        self.create_detail(cheap_offer, price=100, offer_type="standard")
        self.create_detail(cheap_offer, price=200, offer_type="premium")
        expensive_offer = self.create_listing_offer(user, "expensive", price=100)
        response = self.client.get("/api/offers/?min_price=75")
        self.assert_offer_results(response, expensive_offer)

    def test_offer_list_filter_by_max_delivery_time(self):
        user = self.create_user()
        fast_offer = self.create_listing_offer(user, "fast", delivery_time=3)
        self.create_listing_offer(user, "slow", delivery_time=10)
        response = self.client.get("/api/offers/?max_delivery_time=5")
        self.assert_offer_results(response, fast_offer)

    def test_offer_list_search(self):
        user = self.create_user()
        matching_offer = self.create_listing_offer(user, "Logo Design")
        self.create_listing_offer(user, "Webseite")
        response = self.client.get("/api/offers/?search=logo")
        self.assert_offer_results(response, matching_offer)

    def test_offer_list_search_description(self):
        user = self.create_user()
        matching_offer = self.create_listing_offer(
            user, "titletest", description="test logo"
        )
        self.create_listing_offer(user, "Webseite")
        response = self.client.get("/api/offers/?search=logo")
        self.assert_offer_results(response, matching_offer)

    def test_offer_list_ordering_by_updated_at(self):
        user = self.create_user()
        older_offer = self.create_listing_offer(user, "older")
        newer_offer = self.create_listing_offer(user, "newer")
        response = self.client.get("/api/offers/?ordering=updated_at")
        self.assert_offer_results(response, older_offer, newer_offer)

    def test_offer_list_ordering_by_min_price(self):
        user = self.create_user()
        cheap_offer = self.create_listing_offer(user, "cheap", price=50)
        expensive_offer = self.create_listing_offer(user, "expensive", price=100)
        response = self.client.get("/api/offers/?ordering=min_price")
        self.assert_offer_results(response, cheap_offer, expensive_offer)

    def test_offer_list_page_size(self):
        user = self.create_user()
        self.create_listing_offer(user, "cheap", price=50)
        self.create_listing_offer(user, "expensive", price=100)
        response = self.client.get("/api/offers/?page_size=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 1)


class OfferDetailRetrieveViewTest(OfferTestMixin, APITestCase):
    def test_offerdetail_retrieve_success(self):
        user = self.create_user("createcust", "customer")
        detail = self.create_detail(self.create_offer(user))
        self.client.force_authenticate(user=user)
        response = self.client.get(f"/api/offerdetails/{detail.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OfferDetailViewTest(OfferTestMixin, APITestCase):
    def test_offer_retrieve_success(self):
        owner = self.create_user("retrieveowner")
        offer = self.create_package_offer(owner)
        self.client.force_authenticate(user=owner)
        response = self.client.get(f"/api/offers/{offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_offer_retrieve_unauthenticated(self):
        offer = self.create_package_offer(self.create_user("retrieveowner2"))
        response = self.client.get(f"/api/offers/{offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_patch_owner_success(self):
        owner = self.create_user("patchowner")
        offer = self.create_package_offer(owner)
        self.client.force_authenticate(user=owner)
        response = self.client.patch(
            f"/api/offers/{offer.id}/", self._patch_data(), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_offer_patch_forbidden_for_non_owner(self):
        offer = self.create_package_offer(self.create_user("patchowner2"))
        self.client.force_authenticate(user=self.create_user("patchother2"))
        response = self.client.patch(f"/api/offers/{offer.id}/", {"title": "Hacked"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_delete_owner_success(self):
        owner = self.create_user("deleteowner")
        offer = self.create_package_offer(owner)
        self.client.force_authenticate(user=owner)
        response = self.client.delete(f"/api/offers/{offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_offer_delete_forbidden_for_non_owner(self):
        offer = self.create_package_offer(self.create_user("deleteowner2"))
        self.client.force_authenticate(user=self.create_user("deleteother2"))
        response = self.client.delete(f"/api/offers/{offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_patch_unauthenticated(self):
        offer = self.create_package_offer(self.create_user("patchowner3"))
        response = self.client.patch(f"/api/offers/{offer.id}/", {"title": "Hacked"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_delete_unauthenticated(self):
        offer = self.create_package_offer(self.create_user("deleteowner3"))
        response = self.client.delete(f"/api/offers/{offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def _patch_data(self):
        return {"title": "Updated", "details": [{"offer_type": "basic", "price": 150}]}
