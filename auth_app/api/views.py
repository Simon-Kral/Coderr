from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from ..models import CustomerProfile, BusinessProfile
from .serializers import UserSerializer, RegistrationSerializer, LoginSerializer, FileUploadSerializer, CustomerProfileSerializer, BusinessProfileSerializer, CustomerProfileDetailSerializer, BusinessProfileDetailSerializer
from .permissions import ReadOnly
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from coderr_project.utils import create_profile, get_profile_by_user_id, get_profile_serializer


class RegistrationView(APIView):
    """ 
    RegistrationView handles user registration and token generation.
    It inherits from ObtainAuthToken to simplify token handling.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """ 
        Registers a new user, sets their password, and creates an authentication token.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            saved_account = serializer.save()
            profile = create_profile(type=request.data['type'], user=saved_account, customer_model=CustomerProfile, business_model=BusinessProfile)
            token, created = Token.objects.get_or_create(user=saved_account)
            return Response({'token': token.key, 'user_id': profile.pk, 'username': saved_account.username, 'email': saved_account.email}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """ 
    LoginView handles user login by verifying credentials and returning a token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """ 
        Authenticates the user and returns an authentication token if successful.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            profile = get_profile_by_user_id(id=user.pk, customer_model=CustomerProfile, business_model=BusinessProfile)
            return Response({'token': token.key, 'user_id': profile.pk, 'username': user.username, 'email': user.email}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = get_profile_by_user_id(id=pk, customer_model=CustomerProfile, business_model=BusinessProfile)
            profile_serializer = get_profile_serializer(
                profile=profile,
                customer_serializer=CustomerProfileDetailSerializer,
                business_serializer=BusinessProfileDetailSerializer
            )
            user = profile.user
            user_serializer = UserSerializer(user)
            response_data = profile_serializer.data
            response_data.update(user_serializer.data)
            return Response(response_data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)


class CustomerProfileView(ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReadOnly]

    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer


class BusinessProfileView(ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReadOnly]

    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer


class FileUploadView(APIView):
    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
