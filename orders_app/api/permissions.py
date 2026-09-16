from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == "customer"


class IsOrderBusinessUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_business_user = request.user.type == "business"
        return is_business_user and obj.business_user == request.user
