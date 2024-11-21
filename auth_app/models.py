from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Abstract base class for user profiles. 
    It contains common fields that will be inherited by other profile types (CustomerProfile, BusinessProfile).
    """
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/avatars/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Marks this class as abstract, meaning it won't create its own table
        # but will be used as a base for other models.
        abstract = True


class CustomerProfile(UserProfile):
    """
    Model for customer profiles. Inherits from UserProfile.
    Associates a customer profile with a User object.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_profile')

    @property
    def type(self):
        """
        Returns the profile type as 'customer'.
        """
        return 'customer'


class BusinessProfile(UserProfile):
    """
    Model for business profiles. Inherits from UserProfile.
    Associates a business profile with a User object and provides additional business-related fields.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_profile')
    location = models.CharField(max_length=50, blank=True, null=True)
    tel = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    working_hours = models.CharField(max_length=20, blank=True, null=True)

    @property
    def type(self):
        """
        Returns the profile type as 'business'.
        """
        return 'business'
