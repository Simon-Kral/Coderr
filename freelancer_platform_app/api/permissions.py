from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsBusinessUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.business_profile.exists()


class IsCustomerUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.customer_profile.exists()
