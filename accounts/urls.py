from django.urls import path
from .views import ResgisterEmployee
from .web_views import Register
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api/register", ResgisterEmployee.as_view(), name="employee_register"),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path("registerform", Register.as_view(), name="temp_register"),

]