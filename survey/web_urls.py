"""Survey App Web_urls."""
from django.urls import path
from .web_veiw import SurveyView, SurveyAnswerFormView, SubmittedSurveyListView

urlpatterns = [
    path("listsurvey", SurveyView.as_view(), name="list_survey"),
    path("submitedsurvey", SubmittedSurveyListView.as_view(), name="submited_survey"),
    path("survey/<int:survey_id>", SurveyAnswerFormView.as_view(), name="survey"),

]