"""Accounts App Urls."""
from django.urls import path
from .views import SurveyView, SurveyAnswer, SubmitedSurveyView, DetailSurveyView

urlpatterns = [
    path("survey/", SurveyView.as_view(), name="employee_survey"),
    path("survey/<int:pk>/", DetailSurveyView.as_view(), name="question_detail"),
    path("submit-survey/", SurveyAnswer.as_view(), name="submit_survey"),
    path("submitted-survey/", SubmitedSurveyView.as_view(), name="view_submit_survey"),
]
