"""Accounts App Models."""
from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel


class Employee(BaseModel):
    """
    Employee model extending the BaseModel.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    job_title = models.CharField(max_length=50)
    department = models.CharField(max_length=50)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return self.user.username
