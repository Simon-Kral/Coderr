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


class OfferTests(DefaultCases):
    serializer = OfferSerializer

    def setUp(self):
        self.user_data_customer = {
            'username': 'stefan_customer',
            'password': '123456789',
            'repeated_password': '123456789',
            'email': 'test@mail.com',
            'type': 'customer',
        }
        self.user_data_business = {
            'username': 'stefan_business',
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

    def test_post_offer(self):
        url = reverse('offers')
        data = {
            "title": "Grafikdesign-Paket",
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100.00,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200.00,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500.00,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
                    "offer_type": "premium"
                }
            ]
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        detail_data = OfferDetail.objects.filter(offer=response.data['id'])
        self.assertEqual(3, len(detail_data))
        for detail in detail_data:
            self.assertGreaterEqual(len(detail.features), 1)
        offer_types = set(detail.offer_type for detail in detail_data)
        self.assertEqual(offer_types, {'basic', 'standard', 'premium'})
