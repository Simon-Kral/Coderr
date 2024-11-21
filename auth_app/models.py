from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/avatars/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomerProfile(UserProfile):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_profile')

    @property
    def type(self):
        return 'customer'


class BusinessProfile(UserProfile):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_profile')

    location = models.CharField(max_length=50, blank=True, null=True)
    tel = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    working_hours = models.CharField(max_length=20, blank=True, null=True)

    @property
    def type(self):
        return 'business'
