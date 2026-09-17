from django.db.models import Q
from django.http import Http404
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.models import User

from ..models import Order
from .permissions import IsCustomerUser, IsOrderBusinessUser
from .serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    OrderStatusSerializer,
)


class OrderListCreateView(generics.ListCreateAPIView):
    """Lists user orders and creates new orders."""
    serializer_class = OrderSerializer

    def get_queryset(self):
        """Returns orders related to the request user."""
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        )

    def get_serializer_class(self):
        """Selects the serializer for the request method."""
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        """Selects permissions for reading or creating orders."""
        permission_list = [permissions.IsAuthenticated()]
        if self.request.method == "POST":
            permission_list.append(IsCustomerUser())
        return permission_list


class OrderDetailView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """Updates or deletes a single order."""
    queryset = Order.objects.all()

    def get_serializer_class(self):
        """Returns the serializer for order changes."""
        return OrderStatusSerializer

    def get_permissions(self):
        """Selects permissions for updating or deleting orders."""
        if self.request.method == "PATCH":
            return [permissions.IsAuthenticated(), IsOrderBusinessUser()]
        return [permissions.IsAuthenticated(), permissions.IsAdminUser()]

    def patch(self, request, *args, **kwargs):
        """Updates part of an order."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Deletes an order."""
        return self.destroy(request, *args, **kwargs)


class BaseOrderCountView(APIView):
    """Provides a count of orders with one status."""
    permission_classes = [permissions.IsAuthenticated]
    status_value = ""
    response_key = ""

    def get(self, request, business_user_id):
        """Returns the order count for a business user."""
        self._check_business_user(business_user_id)
        order_count = Order.objects.filter(
            business_user_id=business_user_id,
            status=self.status_value,
        ).count()
        return Response({self.response_key: order_count})

    def _check_business_user(self, business_user_id):
        """Checks that the requested user is a business user."""
        user_exists = User.objects.filter(
            id=business_user_id,
            type="business",
        ).exists()
        if not user_exists:
            raise Http404


class OrderCountView(BaseOrderCountView):
    """Provides the count of active orders."""
    status_value = "in_progress"
    response_key = "order_count"


class CompletedOrderCountView(BaseOrderCountView):
    """Provides the count of completed orders."""
    status_value = "completed"
    response_key = "completed_order_count"
