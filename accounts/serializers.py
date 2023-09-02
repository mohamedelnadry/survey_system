"""Accounts App Serializer."""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Employee


class RegisterEmployeeSerializer(serializers.Serializer):
    """
    Serializer for employee registration.
    """

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    job_title = serializers.CharField(max_length=50)
    department = serializers.CharField(max_length=50)

    def validate_username(self, value):
        """
        Validate the username field to ensure uniqueness.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username Already Exists.")
        return value
