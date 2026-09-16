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
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        permission_list = [permissions.IsAuthenticated()]
        if self.request.method == "POST":
            permission_list.append(IsCustomerUser())
        return permission_list


class OrderDetailView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        return OrderStatusSerializer

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [permissions.IsAuthenticated(), IsOrderBusinessUser()]
        return [permissions.IsAuthenticated(), permissions.IsAdminUser()]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BaseOrderCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    status_value = ""
    response_key = ""

    def get(self, request, business_user_id):
        self._check_business_user(business_user_id)
        order_count = Order.objects.filter(
            business_user_id=business_user_id,
            status=self.status_value,
        ).count()
        return Response({self.response_key: order_count})

    def _check_business_user(self, business_user_id):
        user_exists = User.objects.filter(
            id=business_user_id,
            type="business",
        ).exists()
        if not user_exists:
            raise Http404


class OrderCountView(BaseOrderCountView):
    status_value = "in_progress"
    response_key = "order_count"


class CompletedOrderCountView(BaseOrderCountView):
    status_value = "completed"
    response_key = "completed_order_count"
