from django.contrib.auth import get_user_model
from offers_app.models import Offer, OfferDetail


class OfferTestMixin:
    def create_user(self, username="business", user_type="business"):
        return get_user_model().objects.create_user(
            username=username, password="testpass123", type=user_type
        )

    def create_offer(self, user, title="testtitle", description="testdescription"):
        return Offer.objects.create(user=user, title=title, description=description)

    def create_detail(
        self, offer, title="testtitle", revisions=2, delivery_time=5,
        price=100, features=None, offer_type="basic"
    ):
        return OfferDetail.objects.create(
            offer=offer, title=title, revisions=revisions,
            delivery_time_in_days=delivery_time, price=price,
            features=features or [], offer_type=offer_type
        )

    def create_listing_offer(self, user, title, price=100, delivery_time=5,
                             description="testdescription"):
        offer = self.create_offer(user, title, description)
        self.create_detail(offer, price=price, delivery_time=delivery_time)
        return offer

    def create_package_offer(self, user, title="testtitle", description="desc"):
        offer = self.create_offer(user, title, description)
        for package in self._package_data():
            self.create_detail(offer, **package)
        return offer

    def offer_data(self, detail_count=3):
        return {
            "title": "Grafikdesign-Paket",
            "description": "Ein Angebot mit drei Paketen",
            "details": self._detail_data()[:detail_count],
        }

    def _package_data(self):
        return [
            {"title": "Basic", "revisions": 2, "delivery_time": 5,
             "price": 100, "offer_type": "basic"},
            {"title": "Standard", "revisions": 5, "delivery_time": 7,
             "price": 200, "offer_type": "standard"},
            {"title": "Premium", "revisions": 10, "delivery_time": 10,
             "price": 500, "offer_type": "premium"},
        ]

    def _detail_data(self):
        return [
            {"title": "Basic Design", "revisions": 2,
             "delivery_time_in_days": 5, "price": 100,
             "features": ["Logo Design"], "offer_type": "basic"},
            {"title": "Standard Design", "revisions": 5,
             "delivery_time_in_days": 7, "price": 200,
             "features": ["Logo Design", "Visitenkarte"],
             "offer_type": "standard"},
            {"title": "Premium Design", "revisions": 10,
             "delivery_time_in_days": 10, "price": 500,
             "features": ["Logo Design", "Visitenkarte", "Flyer"],
             "offer_type": "premium"},
        ]
