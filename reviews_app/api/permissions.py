from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """Allows access only for customer users."""

    def has_permission(self, request, view):
        """Checks whether the request user is a customer."""
        return request.user.type == "customer"


class IsReviewOwner(permissions.BasePermission):
    """Allows changes only for the author of a review."""

    def has_object_permission(self, request, view, obj):
        """Checks whether the request user wrote the review."""
        return obj.reviewer == request.user
