from django.contrib.auth import get_user_model
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


class OrderTestMixin:
    def create_user(self, username, user_type="customer"):
        return get_user_model().objects.create_user(
            username=username,
            password="testpass123",
            type=user_type,
        )

    def create_offer_detail(self, business_user, offer_type="basic"):
        offer = self._create_offer(business_user)
        return self._create_detail(offer, offer_type)

    def _create_offer(self, business_user):
        return Offer.objects.create(
            user=business_user,
            title="Logo Design",
            description="Design für ein Logo",
        )

    def _create_detail(self, offer, offer_type):
        return OfferDetail.objects.create(
            offer=offer,
            title="Logo Paket",
            revisions=3,
            delivery_time_in_days=5,
            price=150,
            features=["Logo", "Visitenkarte"],
            offer_type=offer_type,
        )

    def create_order(self, customer_user, business_user, status="in_progress"):
        detail = self.create_offer_detail(business_user)
        return Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status=status,
        )
