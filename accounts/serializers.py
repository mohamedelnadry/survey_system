from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Employee


class RegisterEmployeeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    job_title = serializers.CharField(max_length=50)
    department = serializers.CharField(max_length=50)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username Already Exists.")
        return value

    def create(self, validated_data):
        """
        Create a new user with the validated data.
        """
        username = validated_data.get("username")
        password = validated_data.get("password")
        job_title = validated_data.get("job_title")
        department = validated_data.get("department")
        try:
            user = User.objects.create_user(username=username, password=password)
        except Exception as e:
            raise serializers.ValidationError("Could not create user: {}".format(e))

        if user:
            try:
                employee = Employee.objects.create(
                    user=user, job_title=job_title, department=department
                )
            except Exception as e:
                raise serializers.ValidationError(
                    "Could not create profile: {}".format(e)
                )

        return {
            "id":employee.id,
            "username": employee.user.username,
            "job_title": employee.job_title,
            "department": employee.department,
        }
