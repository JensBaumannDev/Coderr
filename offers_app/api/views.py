from django.db.models import Min, Q
from rest_framework import generics, permissions

from offers_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferCreateSerializer, OfferDetailSerializer
from .pagination import OfferPagination
from .permissions import IsBusinessUser, IsOfferOwnerOrReadOnly


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
        queryset = Offer.objects.all()
        queryset = self._add_offer_minimums(queryset)
        queryset = self._filter_queryset(queryset)
        return self._order_queryset(queryset)

    def _add_offer_minimums(self, queryset):
        """Adds minimum values from offer packages."""
        return queryset.annotate(
            lowest_price=Min("details__price"),
            shortest_delivery_time=Min("details__delivery_time_in_days"),
        )

    def _filter_queryset(self, queryset):
        """Applies all supported offer filters."""
        parameters = self.request.query_params
        queryset = self._filter_creator(queryset, parameters.get("creator_id"))
        queryset = self._filter_price(queryset, parameters.get("min_price"))
        queryset = self._filter_delivery_time(
            queryset, parameters.get("max_delivery_time")
        )
        return self._filter_search(queryset, parameters.get("search"))

    def _filter_creator(self, queryset, creator_id):
        """Filters offers by their creator."""
        if creator_id:
            return queryset.filter(user_id=creator_id)
        return queryset

    def _filter_price(self, queryset, min_price):
        """Filters offers by their minimum price."""
        if min_price:
            return queryset.filter(lowest_price__gte=min_price)
        return queryset

    def _filter_delivery_time(self, queryset, max_delivery_time):
        """Filters offers by their shortest delivery time."""
        if max_delivery_time:
            return queryset.filter(shortest_delivery_time__lte=max_delivery_time)
        return queryset

    def _filter_search(self, queryset, search):
        """Searches offer titles and descriptions."""
        if search:
            return queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return queryset

    def _order_queryset(self, queryset):
        """Orders offers by the requested supported field."""
        ordering = self.request.query_params.get("ordering")
        if ordering == "min_price":
            return queryset.order_by("lowest_price")
        if ordering == "updated_at":
            return queryset.order_by(ordering)
        return queryset.order_by("-created_at")


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
