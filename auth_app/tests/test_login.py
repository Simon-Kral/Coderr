from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token


class LoginTests(APITestCase):
    url = reverse('login')

    def setUp(self):
        self.user_data = {
            'username': 'stefan',
            'password': '123456789',
            'repeated_password': '123456789',
            'email': 'test@mail.com',
            'type': 'customer',
        }
        self.user = User.objects.create_user(
            username=self.user_data['username'], password=self.user_data['password'], email=self.user_data['email'],)
        self.token = Token.objects.create(user=self.user)

    def test_login(self):
        data = {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'token')
        self.assertContains(response, 'username')
        self.assertContains(response, 'email')
        self.assertContains(response, 'user_id')

    def test_wrong_password(self):
        data = {
            'username': self.user_data['username'],
            'password': self.user_data['password'] + 'test',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_email(self):
        data = {
            'username': self.user_data['username'] + 'test',
            'password': self.user_data['password'],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
