from rest_framework import status, generics, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min, Avg
from django.contrib.auth.models import User
from auth_app.models import BusinessProfile
from ..models import Offer, OfferDetail, Order, Review
from .serializers import OfferSerializer, OfferDetailSerializer, DetailsSerializer, OrderSerializer, ReviewSerializer
from .filters import OfferFilter
from .pagination import OfferPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from coderr_project.permissions import ReadOnly, Forbidden, IsAdmin, IsStaff, IsOwner, IsBusinessUser, IsCustomerUser


class OfferListView(generics.ListCreateAPIView):
    """
    Handles listing and creating offers. Supports filtering, searching, and pagination.
    Different permissions are applied based on the request method.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = []

    queryset = Offer.objects.all().annotate(min_price=Min('details__price'))  # Annotates the offers with their minimum price
    serializer_class = OfferSerializer

    # Enables filtering, searching, and ordering for offers
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    search_fields = ['title', 'description']
    pagination_class = OfferPagination

    def get_permissions(self):
        """
        Dynamically sets permissions based on the request method.
        - GET: Accessible to everyone.
        - POST: Restricted to admins and business users.
        """
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdmin | IsBusinessUser]
        return super(OfferListView, self).get_permissions()


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting specific offers.
    Applies dynamic permissions based on the request method.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = []

    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Deletes the specified offer and returns a success response.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """
        Dynamically sets permissions:
        - GET: Accessible to everyone.
        - PUT: Forbidden.
        - PATCH/DELETE: Restricted to admins and owners.
        """
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        if self.request.method == 'PUT':
            self.permission_classes = [Forbidden]
        if self.request.method in ['PATCH', 'DELETE']:
            self.permission_classes = [IsAdmin | IsOwner]
        return super(OfferDetailView, self).get_permissions()


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting offer details.
    Permissions are set to allow admins, owners, and read-only access.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin | IsOwner | ReadOnly]

    queryset = OfferDetail.objects.all()
    serializer_class = DetailsSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    Manages orders, including listing, creating, and updating them.
    Filters accessible orders based on the user's role (customer or business user).
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = []

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        Returns orders relevant to the requesting user.
        - Superusers see all orders.
        - Customers and business users see orders they are involved in.
        """
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(customer_user=user) | Order.objects.filter(offer_details__offer__user=user)

    def get_permissions(self):
        """
        Dynamically sets permissions based on the request method.
        - GET: Requires authentication.
        - POST: Restricted to admins and customer users.
        - PUT: Forbidden.
        - PATCH: Restricted to admins and owners.
        - DELETE: Restricted to admins.
        """
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdmin | IsCustomerUser]
        if self.request.method == 'PUT':
            self.permission_classes = [Forbidden]
        if self.request.method == 'PATCH':
            self.permission_classes = [IsAdmin | IsOwner]
        if self.request.method == 'DELETE':
            self.permission_classes = [IsAdmin]
        return super(OrderViewSet, self).get_permissions()

    def destroy(self, request, *args, **kwargs):
        """
        Deletes the specified order and returns a success response.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Handles listing, creating, updating, and deleting reviews.
    Supports filtering by business user and reviewer, and ordering by date or rating.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = []

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # Enables filtering and ordering for reviews
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']

    def get_permissions(self):
        """
        Dynamically sets permissions based on the request method.
        - GET: Requires authentication.
        - POST: Restricted to admins and customer users.
        - PUT: Forbidden.
        - PATCH: Restricted to admins and owners.
        - DELETE: Restricted to staff and owners.
        """
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdmin | IsCustomerUser]
        if self.request.method == 'PUT':
            self.permission_classes = [Forbidden]
        if self.request.method == 'PATCH':
            self.permission_classes = [IsAdmin | IsOwner]
        if self.request.method == 'DELETE':
            self.permission_classes = [IsStaff | IsOwner]
        return super(ReviewViewSet, self).get_permissions()


class BaseInfoView(APIView):
    """
    Provides aggregated statistics about the platform, such as review count, average rating,
    number of business profiles, and total offers.
    """
    def get(self, request):
        # Retrieve platform statistics
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']
        average_rating = round(average_rating, 1) if average_rating is not None else 0.0
        business_profile_count = BusinessProfile.objects.count()
        offer_count = Offer.objects.count()

        # Return the aggregated data
        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }
        return Response(data, status=status.HTTP_200_OK)


class OrderCountView(APIView):
    """
    Returns the count of in-progress orders for a specific business user.
    """
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            order_count = Order.objects.filter(offer_details__offer__user=user, status='in_progress').count()
            return Response({'order_count': order_count}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Business user not found.'}, status=status.HTTP_404_NOT_FOUND)


class CompletedOrderCountView(APIView):
    """
    Returns the count of completed orders for a specific business user.
    """
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            completed_order_count = Order.objects.filter(offer_details__offer__user=user, status='completed').count()
            return Response({'completed_order_count': completed_order_count}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Business user not found.'}, status=status.HTTP_404_NOT_FOUND)
