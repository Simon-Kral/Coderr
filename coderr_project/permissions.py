from rest_framework.permissions import BasePermission, SAFE_METHODS
from freelancer_platform_app.models import OfferDetail, Order, Review


class ReadOnly(BasePermission):
    """
    Permission class allowing read-only access.

    Methods:
        - has_permission: Grants access if the request method is safe (e.g., GET, HEAD, OPTIONS).
        - has_object_permission: Grants access to individual objects if the request method is safe.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class Forbidden(BasePermission):
    """
    Permission class denying all access.

    Methods:
        - has_permission: Always returns False, denying access at the global level.
        - has_object_permission: Always returns False, denying access to individual objects.
    """

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class IsAdmin(BasePermission):
    """
    Permission class granting access only to admin users.

    Methods:
        - has_permission: Returns True if the user is a superuser.
        - has_object_permission: Grants access to individual objects if the user is a superuser.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsStaff(BasePermission):
    """
    Permission class granting access only to staff users.

    Methods:
        - has_permission: Returns True if the user is staff.
        - has_object_permission: Grants access to individual objects if the user is staff.
    """

    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class IsOwner(BasePermission):
    """
    Permission class granting access only to the owner of the resource.

    Methods:
        - has_object_permission: Checks ownership for different types of objects:
            - For OfferDetail: Checks if the user owns the associated offer.
            - For Order: Checks if the user owns the associated offer via the offer details.
            - For other objects: Checks if the user is directly the owner.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, OfferDetail):
            return request.user == obj.offer.user
        elif isinstance(obj, Order):
            return request.user == obj.offer_details.offer.user
        elif isinstance(obj, Review):
            return request.user == obj.reviewer
        else:
            return request.user == obj.user


class IsBusinessUser(BasePermission):
    """
    Permission class granting access only to business users.

    Methods:
        - has_permission: Returns True if the user has an associated business profile.
        - has_object_permission: Grants access to individual objects if the user has a business profile.
    """

    def has_permission(self, request, view):
        return request.user.business_profile.exists()

    def has_object_permission(self, request, view, obj):
        return request.user.business_profile.exists()


class IsCustomerUser(BasePermission):
    """
    Permission class granting access only to customer users.

    Methods:
        - has_permission: Returns True if the user has an associated customer profile.
        - has_object_permission: Grants access to individual objects if the user has a customer profile.
    """

    def has_permission(self, request, view):
        return request.user.customer_profile.exists()

    def has_object_permission(self, request, view, obj):
        return request.user.customer_profile.exists()
