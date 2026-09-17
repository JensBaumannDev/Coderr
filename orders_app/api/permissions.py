from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """Allows access only for customer users."""

    def has_permission(self, request, view):
        """Checks whether the request user is a customer."""
        return request.user.type == "customer"


class IsOrderBusinessUser(permissions.BasePermission):
    """Allows order changes only for the responsible business user."""

    def has_object_permission(self, request, view, obj):
        """Checks whether the business user owns the order."""
        is_business_user = request.user.type == "business"
        return is_business_user and obj.business_user == request.user
