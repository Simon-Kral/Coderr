from rest_framework import serializers
from ..models import Offer, OfferDetail, Order, Review
from coderr_project.utils import get_hyperlinked_details, get_user_details, get_min_value
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser


class DetailsSerializer(serializers.ModelSerializer):

    class Meta():
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class DetailsHyperlinkedSerializer(DetailsSerializer, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']


class OfferSerializer(serializers.ModelSerializer):

    details = DetailsSerializer(many=True)

    class Meta():
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description',  'created_at', 'updated_at', 'details']
        read_only_fields = ['user', 'created_at', 'updated_at', 'min_price', 'min_delivery_time']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            if not isinstance(self.context['request'].user, AnonymousUser):
                representation['user_details'] = get_user_details(self.context['request'].user)
            representation['details'] = get_hyperlinked_details(instance, self.context['request'], DetailsHyperlinkedSerializer)
            representation['min_price'] = get_min_value(instance.details, 'price')
            representation['min_delivery_time'] = get_min_value(instance.details, 'delivery_time_in_days')

        return representation

    def validate(self, attrs):
        detail_data = self.initial_data.get('details')
        if len(detail_data) != 3:
            raise serializers.ValidationError("Exactly 3 offer-details are required.")

        needed_types = {'basic', 'standard', 'premium'}
        provided_types = {detail['offer_type'] for detail in detail_data}

        if needed_types != provided_types:
            raise serializers.ValidationError(
                "The offer must contain exactly one 'basic', 'standard', and 'premium' detail."
            )

        return attrs

    def create(self, validated_data):
        detail_data = validated_data.pop('details')
        user = self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)
        for detail in detail_data:
            detail = OfferDetail.objects.create(offer=offer, **detail)
        return offer


class OfferDetailSerializer(serializers.ModelSerializer):

    details = DetailsSerializer(many=True)

    class Meta():
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description',  'created_at', 'updated_at', 'details']
        read_only_fields = ['user', 'created_at', 'updated_at', 'min_price', 'min_delivery_time']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            representation['user_details'] = get_user_details(self.context['request'].user)
            representation['min_price'] = get_min_value(instance.details, 'price')
            representation['min_delivery_time'] = get_min_value(instance.details, 'delivery_time_in_days')
        return representation

    def update(self, instance, validated_data):
        if 'details' in validated_data:
            detail_data = validated_data.pop('details')
            for detail in detail_data:
                offer_type = detail.get('offer_type')
                detail_instance = instance.details.filter(offer_type=offer_type).first()
                super().update(detail_instance, detail)
        instance = super().update(instance, validated_data)
        return instance


class OrderSerializer(serializers.ModelSerializer):
    business_user = serializers.SerializerMethodField()

    class Meta():
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']
        read_only_fields = ['customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'created_at', 'updated_at']

    def create(self, validated_data):
        details = OfferDetail.objects.get(pk=self.initial_data.get('offer_detail_id'))
        user = self.context['request'].user
        order = Order.objects.create(customer_user=user, offer_details=details)
        return order

    def get_business_user(self, obj):
        return obj.business_user.id


class ReviewSerializer(serializers.ModelSerializer):

    class Meta():
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['business_user', 'reviewer', 'created_at', 'updated_at']

    def create(self, validated_data):
        reviewer = self.context['request'].user
        business_user = User.objects.get(pk=self.initial_data['business_user'])
        review = Review.objects.create(reviewer=reviewer, business_user=business_user, **validated_data)
        return review
