from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Offer(models.Model):
    """ 
    Represents an offer created by a user. Contains essential details such as title, image, and description.
    Tracks the creation and last updated timestamps.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='uploads/offer_images/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OfferDetail(models.Model):
    """ 
    Represents detailed information about an offer, including pricing tiers and specific features.
    Each offer can have multiple details (e.g., basic, standard, premium).
    """
    TYPE_CHOICES = (
        ("basic", "basic"),
        ("standard", "standard"),
        ("premium", "premium"),
    )

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=1, validators=[MinValueValidator(-1)])
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    features = models.JSONField()
    offer_type = models.CharField(max_length=8, choices=TYPE_CHOICES)

    class Meta:
        unique_together = ['offer', 'offer_type']


class Order(models.Model):
    """ 
    Represents an order placed by a customer for a specific offer detail.
    Tracks the status of the order and related timestamps.
    """
    TYPE_CHOICES = (
        ("basic", "basic"),
        ("standard", "standard"),
        ("premium", "premium"),
    )
    STATUS_CHOICES = (
        ("in_progress", "in_progress"),
        ("completed", "completed"),
        ("cancelled", "cancelled"),
    )

    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_customer')
    status = models.CharField(default='in_progress', max_length=11, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    offer_details = models.ForeignKey(OfferDetail, on_delete=models.CASCADE, related_name='order_details')

    # Computed properties to provide convenient access to related fields
    @property
    def business_user(self):
        """ Returns the user who created the offer related to this order. """
        return self.offer_details.offer.user

    @property
    def title(self):
        """ Returns the title of the offer related to this order. """
        return self.offer_details.offer.title

    @property
    def revisions(self):
        """ Returns the number of revisions allowed for this order. """
        return self.offer_details.revisions

    @property
    def delivery_time_in_days(self):
        """ Returns the delivery time in days for this order. """
        return self.offer_details.delivery_time_in_days

    @property
    def price(self):
        """ Returns the price of this order. """
        return self.offer_details.price

    @property
    def features(self):
        """ Returns the features of this order. """
        return self.offer_details.features

    @property
    def offer_type(self):
        """ Returns the type of the offer detail for this order (basic/standard/premium). """
        return self.offer_details.offer_type


class Review(models.Model):
    """ 
    Represents a review given by a customer to a business user.
    Includes a rating, description, and timestamps for tracking creation and updates.
    """
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_business')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_customer')
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['reviewer', 'business_user']
