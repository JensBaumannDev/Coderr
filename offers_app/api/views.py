from rest_framework import generics, permissions
from offers_app.models import Offer
from .serializers import OfferSerializer, OfferCreateSerializer
from .pagination import OfferPagination
from .permissions import IsBusinessUser


class OfferListView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    pagination_class = OfferPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.AllowAny()]
