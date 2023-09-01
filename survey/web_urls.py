from django.urls import path
from .web_veiw import SurveyView

urlpatterns = [
    path("listsurvey", SurveyView.as_view(), name="list_survey"),
]