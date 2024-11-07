from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(('customer', 'business'))

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        pw = attrs['password']
        repeated_password = attrs['repeated_password']
        type = attrs['type']

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

    def save(self):
        account = User(
            email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(self.validated_data['password'])
        account.save()
        return account


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['file', 'uploaded_at']
