from django.urls import path, include
from rest_framework import routers
from .views import RegistrationView, LoginView, ProfileDetailView, CustomerProfileView, BusinessProfileView, FileUploadView

# router = routers.SimpleRouter()
# router.register(r'profile/customer', CustomerProfileView, basename='customer-profiles')
# router.register(r'profile/business', BusinessProfileView, basename='business-profiles')

urlpatterns = [
    # path('', include(router.urls)),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/customer/', CustomerProfileView.as_view(), name='customer-profiles'),
    path('profiles/business/', BusinessProfileView.as_view(), name='business-profiles'),
]
