from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import CustomerProfile, BusinessProfile
from coderr_project.utils import get_user_details

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model. Provides basic user details such as username,
    email, first name, and last name.
    """
    class Meta(object):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class RegistrationSerializer(serializers.Serializer):
    """
    Serializer for user registration. Handles validation of the provided 
    username, email, and password, as well as the account type (customer/business).
    """
    username = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(('customer', 'business'))

    def validate(self, attrs):
        """
        Validates the registration data, ensuring that:
        - The username is unique
        - The passwords match
        - The account type is valid (either 'customer' or 'business')
        """
        pw = attrs.get('password')
        repeated_password = attrs.get('repeated_password')

        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                {'error': 'A user with this username already exists.'})
        if pw != repeated_password:
            raise serializers.ValidationError(
                {'error': 'Passwords don\'t match.'})
        return attrs

    def create(self, validated_data):
        """
        Creates a new user account using the validated data, 
        including setting the password and saving the account.
        """
        account = User(email=validated_data['email'], username=validated_data['username'])
        account.set_password(self.validated_data['password'])
        account.save()
        return account


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login. Validates the username and password for authentication.
    """
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, attrs):
        """
        Validates that the username exists and the password is correct.
        """
        username = attrs.get('username')
        password = attrs.get('password')
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error': 'Username not found.'})
        self.user = User.objects.get(username=username)
        if not self.user.check_password(password):
            raise serializers.ValidationError({'error': 'Wrong password.'})
        return attrs

    def create(self, validated_data):
        """
        Returns the authenticated user after successful login.
        """
        return self.user


class CustomerProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomerProfile model. Provides basic details 
    such as the user, creation timestamp, uploaded file, and type.
    """
    class Meta:
        model = CustomerProfile
        fields = ['user', 'created_at', 'file', 'uploaded_at', 'type']


class BusinessProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the BusinessProfile model. Provides details such as 
    the user, creation timestamp, uploaded file, business location, 
    telephone number, description, working hours, and type.
    """
    class Meta:
        model = BusinessProfile
        fields = ['user', 'created_at', 'file', 'uploaded_at', 'location', 'tel', 'description', 'working_hours', 'type']


class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomerProfile model. Customizes the representation 
    of user details based on the request method.
    """
    class Meta:
        model = CustomerProfile
        fields = ['user', 'created_at', 'file', 'uploaded_at', 'type']

    def to_representation(self, instance):
        """
        Customizes the representation of the CustomerProfile model by adding 
        user details for GET requests, and includes user primary key.
        """
        representation = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            user = User.objects.get(pk=representation.pop('user'))
            representation['user'] = get_user_details(user)
            representation['user']['pk'] = user.id
        return representation


class BusinessProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the BusinessProfile model. Customizes the representation 
    of user details and other business-related fields.
    """
    class Meta:
        model = BusinessProfile
        fields = ['user', 'created_at', 'file', 'uploaded_at', 'location', 'tel', 'description', 'working_hours', 'type']

    def to_representation(self, instance):
        """
        Customizes the representation of the BusinessProfile model by adding 
        user details for GET requests, and includes user primary key.
        """
        representation = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            user = User.objects.get(pk=representation.pop('user'))
            representation['user'] = get_user_details(user)
            representation['user']['pk'] = user.id
        return representation
