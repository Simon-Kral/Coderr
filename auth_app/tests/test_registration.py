from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .default_tests import DefaultCases
from ..api.serializers import RegistrationSerializer
from ..models import CustomerProfile, BusinessProfile
from coderr_project.utils import get_profile_by_user_username


class RegistrationTests(DefaultCases):
    url = reverse('registration')
    serializer = RegistrationSerializer

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'secret',
            'repeated_password': 'secret',
            'email': 'test@mail.com',
            'type': 'customer',
        }

    def test_registration(self):
        response = self.client.post(self.url, self.user_data)
        fields = {'token', 'username', 'email', 'user_id'}
        self.http_status_test(resp=response, status=status.HTTP_201_CREATED)
        self.contains_fields_test(resp=response, fields=fields, status=status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['user_id'],
            get_profile_by_user_username(
                username=self.user_data['username'],
                customer_model=CustomerProfile,
                business_model=BusinessProfile
            ).id,
        )

    def test_username_already_exists(self):
        self.client.post(self.url, self.user_data)
        error_message = 'A user with this username already exists.'
        self.error_tests(ser=self.serializer, data=self.user_data, status=status.HTTP_400_BAD_REQUEST, msg=error_message)

    def test_passwords_dont_match(self):
        data_to_change = {
            'username': self.user_data['username'] + '_test_passwords_dont_match',
            'repeated_password': self.user_data['repeated_password'] + '_invalid',
        }
        new_user_data = self.user_data
        new_user_data.update(data_to_change)
        error_message = 'Passwords don\'t match.'
        self.error_tests(ser=self.serializer, data=new_user_data, status=status.HTTP_400_BAD_REQUEST, msg=error_message)

    def test_wrong_type(self):
        data_to_change = {
            'username': self.user_data['username'] + '_test_wrong_type',
            'type': self.user_data['type'] + '_invalid',
        }
        new_user_data = self.user_data
        new_user_data.update(data_to_change)
        error_message = '"' + new_user_data['type'] + '"' + ' is not a valid choice.'
        self.error_tests(ser=self.serializer, data=new_user_data, status=status.HTTP_400_BAD_REQUEST, msg=error_message)
