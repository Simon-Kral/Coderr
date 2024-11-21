from rest_framework.permissions import BasePermission, SAFE_METHODS
from freelancer_platform_app.models import OfferDetail, Order


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class Forbidden(BasePermission):

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, OfferDetail):
            return request.user == obj.offer.user
        elif isinstance(obj, Order):
            return request.user == obj.offer_details.offer.user
        else:
            return request.user == obj.user


class IsBusinessUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.business_profile.exists()

    def has_object_permission(self, request, view, obj):
        return request.user.business_profile.exists()


class IsCustomerUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.customer_profile.exists()

    def has_object_permission(self, request, view, obj):
        return request.user.customer_profile.exists()
