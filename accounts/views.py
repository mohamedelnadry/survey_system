"""Accounts App Views."""
from rest_framework import generics, views, status
from rest_framework.response import Response
from .models import Employee
from django.contrib.auth.models import User
from .serializers import RegisterEmployeeSerializer


class UserRegister(views.APIView):
    """
    APIView for user registration.
    Handles POST requests to create new User and Employee objects.
    """

    def post(self, request):
        """
        Handles POST request to create a new User and Employee.

        Parameters:
            request (HttpRequest): The HTTP request containing the POST data.

        Returns:
            Response: HTTP response containing the created User and Employee data,
                      or errors if the request is invalid.
        """
        serializer = RegisterEmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        job_title = serializer.validated_data["job_title"]
        department = serializer.validated_data["department"]

        employee = self.create_employee(username, password, job_title, department)
        if not employee:
            return Response(
                {"message": "Can't create user, please try again with valid inputs"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def create_employee(username, password, job_title, department):
        """
        Utility method to create a new Employee object along with its associated User.

        Parameters:
            username (str): Username for the new User object.
            password (str): Password for the new User object.
            job_title (str): Job title for the new Employee object.
            department (str): Department for the new Employee object.

        Returns:
            Employee: The created Employee object, or None if creation failed.
        """
        try:
            user = User.objects.create_user(username=username, password=password)
            employee = Employee.objects.create(
                user=user, job_title=job_title, department=department
            )
            return employee
        except Exception as e:
            return None
