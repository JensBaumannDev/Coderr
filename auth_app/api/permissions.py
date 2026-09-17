from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allows changes only for the profile owner."""

    def has_object_permission(self, request, view, obj):
        """Checks whether the request user owns the profile."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
