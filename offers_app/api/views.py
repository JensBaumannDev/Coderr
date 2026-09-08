from rest_framework import generics, permissions
from offers_app.models import Offer
from .serializers import OfferSerializer
from .pagination import OfferPagination


class OfferListView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = OfferPagination
    

