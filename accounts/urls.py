"""Accounts App Urls."""
from django.urls import path
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserRegister
from .web_views import Register, LoginView

urlpatterns = [
    # API endpoints
    path("api/register", UserRegister.as_view(), name="employee_register"),
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),

    # Web form views
    path("registerform", Register.as_view(), name="temp_register"),
    path("login/", LoginView.as_view(), name="login"),
    
    # Logout view
    path("logout/", LogoutView.as_view(next_page="/accounts/login"), name="logout"),
]
