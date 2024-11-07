from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    TYPE_CHOICES = (
        ("customer", "customer"),
        ("business", "business"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    uploaded_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    working_hours = models.CharField(max_length=20, blank=True, null=True)
    tel = models.CharField(max_length=50, blank=True, null=True)
