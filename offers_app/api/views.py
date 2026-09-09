from rest_framework import generics, permissions
from offers_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferCreateSerializer, OfferDetailSerializer
from .pagination import OfferPagination
from .permissions import IsBusinessUser, IsOfferOwnerOrReadOnly


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


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOfferOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return OfferCreateSerializer
        return OfferSerializer
