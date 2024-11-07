from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import FileUploadSerializer
from .models import UserProfile
from rest_framework.authtoken.views import ObtainAuthToken


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
            UserProfile.objects.create(
                user=saved_account, type=request.data['type'])
            token, created = Token.objects.get_or_create(user=saved_account)
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    """ 
    LoginView handles user login by verifying credentials and returning a token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """ 
        Authenticates the user and returns an authentication token if successful.
        """
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.pk,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileUploadView(APIView):
    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
