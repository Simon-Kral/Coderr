from rest_framework import serializers
from ..models import Offer, OfferDetail, Order, Review
from coderr_project.utils import get_hyperlinked_details, get_user_details, get_min_value
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from auth_app.models import BusinessProfile


class DetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for OfferDetail model. Provides basic fields for an offer detail.
    """

    price = serializers.DecimalField(max_digits=15, decimal_places=2, default=0, coerce_to_string=False)

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class DetailsHyperlinkedSerializer(DetailsSerializer, serializers.HyperlinkedModelSerializer):
    """
    Hyperlinked serializer for OfferDetail model, extending DetailsSerializer.
    Used for generating hyperlinks for details.
    """

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f"/offerdetails/{obj.pk}/"



class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for Offer model. Handles serialization of offer details
    and additional fields like minimum price and delivery time.
    """
    details = DetailsSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details']
        read_only_fields = ['user', 'created_at', 'updated_at', 'min_price', 'min_delivery_time']

    def to_representation(self, instance):
        """
        Customizes the representation of the Offer model.
        Adds user details, hyperlinked details, and minimum price/delivery time for GET requests.
        """
        representation = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            if not isinstance(self.context['request'].user, AnonymousUser):
                representation['user_details'] = get_user_details(self.context['request'].user)
            representation['details'] = get_hyperlinked_details(instance, self.context['request'], DetailsHyperlinkedSerializer)
            representation['min_price'] = get_min_value(instance.details, 'price')
            representation['min_delivery_time'] = get_min_value(instance.details, 'delivery_time_in_days')

        return representation

    def validate(self, attrs):
        """
        Validates that the offer contains exactly three details
        with the required types: 'basic', 'standard', and 'premium'.
        """
        detail_data = self.initial_data.get('details')
        if len(detail_data) != 3:
            raise serializers.ValidationError('Exactly 3 offer-details are required.')

        needed_types = {'basic', 'standard', 'premium'}
        provided_types = {detail['offer_type'] for detail in detail_data}

        if needed_types != provided_types:
            raise serializers.ValidationError('The offer must contain exactly one basic, one standard, and one premium detail.')

        return attrs

    def create(self, validated_data):
        """
        Creates a new offer along with its details.
        Associates the offer with the current user.
        """
        detail_data = validated_data.pop('details')
        user = self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)
        for detail in detail_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Offer model, focusing on details serialization.
    Allows updating of nested details.
    """
    details = DetailsSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details']
        read_only_fields = ['user', 'created_at', 'updated_at', 'min_price', 'min_delivery_time']

    def to_representation(self, instance):
        """
        Customizes the representation of the Offer model.
        Adds user details and minimum price/delivery time for GET requests.
        """
        representation = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            representation['user_details'] = get_user_details(self.context['request'].user)
            representation['min_price'] = get_min_value(instance.details, 'price')
            representation['min_delivery_time'] = get_min_value(instance.details, 'delivery_time_in_days')
        return representation

    def update(self, instance, validated_data):
        """
        Updates an offer, including nested details if provided.
        Matches details based on their 'offer_type'.
        """
        if 'details' in validated_data:
            detail_data = validated_data.pop('details')
            for detail in detail_data:
                offer_type = detail.get('offer_type')
                detail_instance = instance.details.filter(offer_type=offer_type).first()
                super().update(detail_instance, detail)
        instance = super().update(instance, validated_data)
        return instance


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model. Adds a method field for the business user
    and restricts writable fields to essential attributes for order creation.
    """
    business_user = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']
        read_only_fields = ['customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Creates a new order for the current user based on the selected offer detail.
        """
        details = OfferDetail.objects.get(pk=self.initial_data.get('offer_detail_id'))
        user = self.context['request'].user
        order = Order.objects.create(customer_user=user, offer_details=details)
        return order

    def get_business_user(self, obj):
        """
        Returns the ID of the business user associated with the order.
        """
        return obj.business_user.id


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model. Allows creating a review
    while associating the current user as the reviewer.
    """
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['business_user', 'reviewer', 'created_at', 'updated_at']

    def validate(self, attrs):
        reviewer = self.context['request'].user

        if self.context['request'].method == "POST":
            if not User.objects.filter(pk=self.initial_data['business_user']).exists():
                raise serializers.ValidationError('Business-user not found.')
            business_user = User.objects.get(pk=self.initial_data['business_user'])
            if not business_user.business_profile.exists():
                raise serializers.ValidationError('You can only write reviews for business users.')

            if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
                raise serializers.ValidationError('You can write only one review per business user.')

        return attrs

    def create(self, validated_data):
        """
        Creates a review for the specified business user, associating the current user as the reviewer.
        """
        reviewer = self.context['request'].user
        business_user = User.objects.get(pk=self.initial_data['business_user'])
        review = Review.objects.create(reviewer=reviewer, business_user=business_user, **validated_data)
        return review
