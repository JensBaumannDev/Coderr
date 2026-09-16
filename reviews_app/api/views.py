from rest_framework import generics, mixins, permissions
from ..models import Review
from .permissions import IsCustomerUser, IsReviewOwner
from .serializers import (
    ReviewCreateSerializer,
    ReviewSerializer,
    ReviewUpdateSerializer,
)


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.all()
        queryset = self._filter_business_user(queryset)
        queryset = self._filter_reviewer(queryset)
        return self._order_queryset(queryset)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_permissions(self):
        permission_list = [permissions.IsAuthenticated()]
        if self.request.method == "POST":
            permission_list.append(IsCustomerUser())
        return permission_list

    def _filter_business_user(self, queryset):
        business_user_id = self.request.query_params.get("business_user_id")
        if business_user_id:
            return queryset.filter(business_user_id=business_user_id)
        return queryset

    def _filter_reviewer(self, queryset):
        reviewer_id = self.request.query_params.get("reviewer_id")
        if reviewer_id:
            return queryset.filter(reviewer_id=reviewer_id)
        return queryset

    def _order_queryset(self, queryset):
        ordering = self.request.query_params.get("ordering")
        allowed_orderings = ["updated_at", "-updated_at", "rating", "-rating"]
        if ordering in allowed_orderings:
            return queryset.order_by(ordering)
        return queryset.order_by("-updated_at")


class ReviewDetailView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsReviewOwner]

    def get_serializer_class(self):
        return ReviewUpdateSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
