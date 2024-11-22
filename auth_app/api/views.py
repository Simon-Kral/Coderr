from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from auth_app.models import BusinessProfile
from ..models import CustomerProfile, BusinessProfile
from .serializers import UserSerializer, RegistrationSerializer, LoginSerializer, CustomerProfileSerializer, BusinessProfileSerializer, CustomerProfileDetailSerializer, BusinessProfileDetailSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from coderr_project.permissions import ReadOnly
from coderr_project.utils import create_profile, get_profile_by_user_id, get_profile_serializer


class RegistrationView(APIView):
    """ 
    Handles user registration and token generation. 
    Inherits from APIView to handle POST requests for registration.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """ 
        Registers a new user, sets their password, and creates an authentication token.
        The user profile is created based on the 'type' (either 'customer' or 'business').
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            saved_account = serializer.save()
            profile = create_profile(type=request.data['type'], user=saved_account, customer_model=CustomerProfile, business_model=BusinessProfile)
            token, created = Token.objects.get_or_create(user=saved_account)
            return Response({
                'token': token.key,
                'user_id': saved_account.pk,
                'username': saved_account.username,
                'email': saved_account.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """ 
    Handles user login and token generation by verifying credentials.
    Inherits from APIView to handle POST requests for login.
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
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """ 
        Fetches user profile details, including the user's information and profile data.
        """
        try:
            profile = get_profile_by_user_id(id=pk, customer_model=CustomerProfile, business_model=BusinessProfile)
            user = profile.user

            user_serializer = UserSerializer(user)
            profile_serializer = get_profile_serializer(
                profile=profile,
                customer_serializer=CustomerProfileDetailSerializer,
                business_serializer=BusinessProfileDetailSerializer
            )

            response_data = profile_serializer.data
            response_data.update(user_serializer.data)
            return Response(response_data, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        """ 
        Allows updating of the user profile details if the user is the profile owner or an admin.
        """
        try:
            profile = get_profile_by_user_id(id=pk, customer_model=CustomerProfile, business_model=BusinessProfile)
            user = User.objects.get(pk=pk)
        except:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_superuser | (request.user == profile.user):
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        data = {key: value for key, value in request.data.items()}
        data.update({'username': user.username})

        user_serializer = UserSerializer(user, data=data)
        user_serializer.update(user, data)

        profile_serializer = get_profile_serializer(
            profile=profile,
            customer_serializer=CustomerProfileDetailSerializer,
            business_serializer=BusinessProfileDetailSerializer,
            data=data,
            partial=True
        )
        profile_serializer.update(profile, data)

        if user_serializer.is_valid():
            if profile_serializer.is_valid():
                response_data = {'email': user_serializer.data['email'], **profile_serializer.data}
                for item in ['user', 'created_at', 'file', 'uploaded_at']:
                    if item in response_data:
                        response_data.pop(item)
                return Response(response_data, status=status.HTTP_200_OK)
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerProfileView(generics.ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReadOnly]

    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer


class BusinessProfileView(generics.ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReadOnly]

    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
