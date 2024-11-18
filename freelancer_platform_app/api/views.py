from rest_framework import status,  viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permissions import ReadOnly, IsAdmin, IsAuthor, IsBusinessUser, IsCustomerUser
from .serializers import OfferSerializer, OfferDetailSerializer, DetailsSerializer, OrderSerializer, ReviewSerializer
from ..models import Offer, OfferDetail, Order, Review
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import Avg
from auth_app.models import BusinessProfile
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import OfferFilter
from .pagination import OfferPagination


class OfferListView(generics.ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsBusinessUser | ReadOnly]

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    search_fields = ['title', 'description']
    pagination_class = OfferPagination


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsBusinessUser | ReadOnly]

    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer


class DetailsView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsBusinessUser | ReadOnly]

    queryset = OfferDetail.objects.all()
    serializer_class = DetailsSerializer


class OrderViewSet(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsCustomerUser | ReadOnly]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsCustomerUser | ReadOnly]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class BaseInfoView(APIView):
    def get(self, request):
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']
        average_rating = round(average_rating, 1) if average_rating is not None else 0.0
        business_profile_count = BusinessProfile.objects.count()
        offer_count = Offer.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }
        return Response(data, status=status.HTTP_200_OK)


class OrderCountView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            order_count = Order.objects.filter(offer_details__offer__user=user, status='in_progress').count()
            return Response({'order_count': order_count}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Business user not found.'}, status=status.HTTP_404_NOT_FOUND)


class CompletedOrderCountView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            completed_order_count = Order.objects.filter(offer_details__offer__user=user, status='completed').count()
            return Response({'order_count': completed_order_count}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Business user not found.'}, status=status.HTTP_404_NOT_FOUND)
