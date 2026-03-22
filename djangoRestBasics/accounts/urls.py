from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts import views

urlpatterns = [
    path('login/', ObtainAuthToken.as_view(), name='login'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('jwt/login/', TokenObtainPairView.as_view(), name='login-jwt'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='refresh-jwt'),
]
