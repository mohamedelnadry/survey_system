"""
URL configuration for project project.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("api/", include("survey.urls")),
    path("", include("survey.web_urls")),
]
