from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import CustomerProfile, BusinessProfile
from coderr_project.utils import get_user_details


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(('customer', 'business'))

    def validate(self, attrs):
        pw = attrs.get('password')
        repeated_password = attrs.get('repeated_password')
        type = attrs.get('type')
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                {'error': 'A user with this username already exists.'})
        if pw != repeated_password:
            raise serializers.ValidationError(
                {'error': 'Passwords don\'t match.'})
        if type not in ['customer', 'business']:
            raise serializers.ValidationError(
                {'error': 'Account type is invalid.'})
        return attrs

    def create(self, validated_data):
        account = User(email=validated_data['email'], username=validated_data['username'])
        account.set_password(self.validated_data['password'])
        account.save()
        return account


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error': 'Username not found.'})
        self.user = User.objects.get(username=username)
        if not self.user.check_password(password):
            raise serializers.ValidationError({'error': 'Wrong password.'})
        return attrs

    def create(self, validated_data):
        return self.user


class CustomerProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['user', 'created_at', 'file', 'uploaded_at', 'type']


class BusinessProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = ['user', 'created_at', 'file', 'uploaded_at', 'location', 'tel', 'description', 'working_hours', 'type']


class CustomerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = ['user', 'created_at', 'file', 'uploaded_at', 'type']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            user = User.objects.get(pk=representation.pop('user'))
            representation['user'] = get_user_details(user)
            representation['user']['pk'] = user.id
        return representation


class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = ['user', 'created_at', 'file', 'uploaded_at', 'location', 'tel', 'description', 'working_hours', 'type']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            user = User.objects.get(pk=representation.pop('user'))
            representation['user'] = get_user_details(user)
            representation['user']['pk'] = user.id
        return representation
