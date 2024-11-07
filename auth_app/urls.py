from django.urls import path, include
from .views import RegistrationView, LoginView, FileUploadView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
]
