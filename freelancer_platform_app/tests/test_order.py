from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .default_tests import DefaultCases
from ..api.serializers import OfferSerializer, DetailsSerializer
from ..models import Offer, OfferDetail, Order, Review
from coderr_project.utils import create_profile
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from auth_app.models import CustomerProfile, BusinessProfile


class OrderTests(DefaultCases):
    serializer = OfferSerializer

    def setUp(self):
        self.user_data_customer = {
            'username': 'user_customer',
            'password': '123456789',
            'repeated_password': '123456789',
            'email': 'test@mail.com',
            'type': 'customer',
        }
        self.user_data_business = {
            'username': 'user_business',
            'password': '123456789',
            'repeated_password': '123456789',
            'email': 'test@mail.com',
            'type': 'business',
        }
        self.user_customer = User.objects.create_user(
            username=self.user_data_customer['username'],
            password=self.user_data_customer['password'],
            email=self.user_data_customer['email'],)

        self.user_business = User.objects.create_user(
            username=self.user_data_business['username'],
            password=self.user_data_business['password'],
            email=self.user_data_business['email'],)

        self.profile_customer = create_profile(type=self.user_data_customer['type'], user=self.user_customer, customer_model=CustomerProfile, business_model=BusinessProfile)
        self.profile_business = create_profile(type=self.user_data_business['type'], user=self.user_business, customer_model=CustomerProfile, business_model=BusinessProfile)

        self.token_customer = Token.objects.create(user=self.user_customer)
        self.token_business = Token.objects.create(user=self.user_business)

        self.client = APIClient()

    # def test_post_order(self):
    #     url = reverse('orders')
    #     data = {
    #         "order_detail_id": 1
    #     }

    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)

    #     response = self.client.post(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     # offer_id = response.data['id']
    #     # self.assertEqual(3, len(OfferDetail.objects.filter(offer=offer_id)))
    #     # self.assertEqual(4, len(Feature.objects.all()))
