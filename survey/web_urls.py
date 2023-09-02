from django.urls import path
from .web_veiw import SurveyView, SurveyAnswerFormView

urlpatterns = [
    path("listsurvey", SurveyView.as_view(), name="list_survey"),
    path("survey/<int:survey_id>", SurveyAnswerFormView.as_view(), name="survey"),

]