from django.db.models import Min, Q
from rest_framework import generics, permissions

from offers_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferCreateSerializer, OfferDetailSerializer
from .pagination import OfferPagination
from .permissions import IsBusinessUser, IsOfferOwnerOrReadOnly


class OfferListView(generics.ListCreateAPIView):
    pagination_class = OfferPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = Offer.objects.all()
        queryset = self._add_offer_minimums(queryset)
        queryset = self._filter_queryset(queryset)
        return self._order_queryset(queryset)

    def _add_offer_minimums(self, queryset):
        return queryset.annotate(
            lowest_price=Min("details__price"),
            shortest_delivery_time=Min("details__delivery_time_in_days"),
        )

    def _filter_queryset(self, queryset):
        parameters = self.request.query_params
        queryset = self._filter_creator(queryset, parameters.get("creator_id"))
        queryset = self._filter_price(queryset, parameters.get("min_price"))
        queryset = self._filter_delivery_time(
            queryset, parameters.get("max_delivery_time")
        )
        return self._filter_search(queryset, parameters.get("search"))

    def _filter_creator(self, queryset, creator_id):
        if creator_id:
            return queryset.filter(user_id=creator_id)
        return queryset

    def _filter_price(self, queryset, min_price):
        if min_price:
            return queryset.filter(lowest_price__gte=min_price)
        return queryset

    def _filter_delivery_time(self, queryset, max_delivery_time):
        if max_delivery_time:
            return queryset.filter(shortest_delivery_time__lte=max_delivery_time)
        return queryset

    def _filter_search(self, queryset, search):
        if search:
            return queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return queryset

    def _order_queryset(self, queryset):
        ordering = self.request.query_params.get("ordering")
        if ordering == "min_price":
            return queryset.order_by("lowest_price")
        if ordering == "updated_at":
            return queryset.order_by(ordering)
        return queryset.order_by("-created_at")


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
