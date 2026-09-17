from rest_framework import generics, permissions

from offers_app.models import Offer, OfferDetail

from .filters import filter_offers
from .pagination import OfferPagination
from .permissions import IsBusinessUser, IsOfferOwnerOrReadOnly
from .serializers import (
    OfferCreateSerializer,
    OfferDetailSerializer,
    OfferSerializer,
)


class OfferListView(generics.ListCreateAPIView):
    """Lists offers and creates new offers."""
    pagination_class = OfferPagination

    def get_serializer_class(self):
        """Selects the serializer for the request method."""
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferSerializer

    def get_permissions(self):
        """Selects permissions for reading or creating offers."""
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        """Builds the filtered and ordered offer list."""
        return filter_offers(Offer.objects.all(), self.request.query_params)


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    """Retrieves one offer package."""
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates, and deletes one offer."""
    queryset = Offer.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOfferOwnerOrReadOnly]

    def get_serializer_class(self):
        """Selects the serializer for the request method."""
        if self.request.method == "PATCH":
            return OfferCreateSerializer
        return OfferSerializer
