from rest_framework import generics
from django.views.generic import CreateView
from .models import Employee
from .serializers import RegisterEmployeeSerializer
# Create your views here.


class ResgisterEmployee(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = RegisterEmployeeSerializer

