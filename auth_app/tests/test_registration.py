from django.db import IntegrityError
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User


class RegistrationTests(APITestCase):
    url = reverse('registration')

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'secret',
            'repeated_password': 'secret',
            'email': 'test@mail.com',
            'type': 'customer',
        }

    def create_new_user(self, user_data):
        User.objects.create_user(user_data)

    def test_registration(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertContains(response, 'token', status_code=201)
        self.assertContains(response, 'username', status_code=201)
        self.assertContains(response, 'email', status_code=201)

    def test_username_already_exists(self):
        self.client.post(self.url, self.user_data)
        self.create_new_user(self.user_data)
        self.assertRaisesRegex(
            IntegrityError, 'UNIQUE constraint failed: auth_user.username', self.create_new_user, self.user_data)

    def test_passwords_dont_match(self):
        new_user_data = self.user_data
        new_user_data['repeated_password'] = self.user_data['repeated_password'] + 'test'
        response = self.client.post(self.url, new_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_type(self):
        new_user_data = self.user_data
        new_user_data['type'] = self.user_data['type'] + 'test'
        response = self.client.post(self.url, new_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
