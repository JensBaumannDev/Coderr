from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """Allows access only for business users."""

    def has_permission(self, request, view):
        """Checks whether the request user is a business user."""
        return request.user.type == "business"


class IsOfferOwnerOrReadOnly(permissions.BasePermission):
    """Allows changes only for the owner of an offer."""

    def has_object_permission(self, request, view, obj):
        """Checks whether the request user owns the offer."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
