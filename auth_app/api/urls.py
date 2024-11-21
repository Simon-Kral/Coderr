from django.urls import path
from .views import RegistrationView, LoginView, ProfileDetailView, CustomerProfileView, BusinessProfileView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/customer/', CustomerProfileView.as_view(), name='customer-profiles'),
    path('profiles/business/', BusinessProfileView.as_view(), name='business-profiles'),
]
