from rest_framework import generics, mixins, permissions

from ..models import Review
from .filters import filter_reviews
from .permissions import IsCustomerUser, IsReviewOwner
from .serializers import (
    ReviewCreateSerializer,
    ReviewSerializer,
    ReviewUpdateSerializer,
)


class ReviewListCreateView(generics.ListCreateAPIView):
    """Lists reviews and creates new reviews."""
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Returns reviews with the requested filters and sorting."""
        return filter_reviews(Review.objects.all(), self.request.query_params)

    def get_serializer_class(self):
        """Selects the serializer for the request method."""
        if self.request.method == "POST":
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_permissions(self):
        """Selects permissions for reading or creating reviews."""
        permission_list = [permissions.IsAuthenticated()]
        if self.request.method == "POST":
            permission_list.append(IsCustomerUser())
        return permission_list

class ReviewDetailView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """Updates or deletes a single review."""
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsReviewOwner]

    def get_serializer_class(self):
        """Returns the serializer for review changes."""
        return ReviewUpdateSerializer

    def patch(self, request, *args, **kwargs):
        """Updates part of a review."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Deletes a review."""
        return self.destroy(request, *args, **kwargs)
