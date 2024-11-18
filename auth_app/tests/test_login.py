from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from .default_tests import DefaultCases
from ..api.serializers import LoginSerializer
from ..models import BusinessProfile, CustomerProfile
from coderr_project.utils import create_profile


class LoginTests(DefaultCases):
    url = reverse('login')
    serializer = LoginSerializer

    def setUp(self):
        self.user_data = {
            'username': 'stefan',
            'password': '123456789',
            'repeated_password': '123456789',
            'email': 'test@mail.com',
            'type': 'customer',
        }
        self.user = User.objects.create_user(username=self.user_data['username'], password=self.user_data['password'], email=self.user_data['email'],)
        self.token = Token.objects.create(user=self.user)
        self.profile = create_profile(type=self.user_data['type'], user=self.user, customer_model=CustomerProfile, business_model=BusinessProfile)

    def test_login(self):
        credentials = {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        }
        fields = {'token', 'id', 'username', 'email', }
        response = self.client.post(self.url, credentials)
        self.http_status_test(resp=response, status=status.HTTP_200_OK)
        self.contains_fields_test(resp=response, fields=fields, status=status.HTTP_200_OK)
        self.assertEqual(response.data['user_id'], CustomerProfile.objects.get(user__username=self.user_data['username']).id)

    def test_wrong_password(self):
        credentials = {
            'username': self.user_data['username'],
            'password': self.user_data['password'] + 'test',
        }
        error_message = 'Wrong password.'
        self.error_tests(ser=self.serializer, data=credentials, status=status.HTTP_400_BAD_REQUEST, msg=error_message)

    def test_wrong_username(self):
        credentials = {
            'username': self.user_data['username'] + 'test',
            'password': self.user_data['password'],
        }
        error_message = 'Username not found.'
        self.error_tests(ser=self.serializer, data=credentials, status=status.HTTP_400_BAD_REQUEST, msg=error_message)
