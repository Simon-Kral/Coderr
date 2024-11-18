from django.urls import path, include
from rest_framework import routers
from .views import OfferListView, OfferDetailView, DetailsView, OrderViewSet, ReviewViewSet, BaseInfoView, OrderCountView, CompletedOrderCountView


router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('offers/', OfferListView.as_view(), name='offers'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offers-detail'),
    path('offerdetails/<int:pk>/', DetailsView.as_view(), name='offerdetail-detail'),
    path('base-info/', BaseInfoView.as_view(), name='base-info'),
    path('order-count/<int:pk>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:pk>/', CompletedOrderCountView.as_view(), name='completed-order-count'),
]
