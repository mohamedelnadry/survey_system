"""Accounts App Admin."""
from django.contrib import admin

from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    """
    Custom admin class for the Employee model.
    """

    list_display = ("user", "job_title", "parent")

    search_fields = ("user__username", "job_title")


admin.site.register(Employee, EmployeeAdmin)
