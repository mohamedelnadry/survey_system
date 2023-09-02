"""Survey App Web_views."""
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, FormView, ListView, TemplateView

from accounts.models import Employee

from .forms import SurveyForm
from .models import Answer, EmployeeServey, Question, Survey


class SurveyView(TemplateView):
    template_name = "survey/list_survey.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        surveys = SurveyView.user_surveys(user=self.request.user)
        context["surveys"] = surveys
        return context

    @staticmethod
    def user_surveys(user):
        employee = Employee.objects.get(user=user)
        surveys = EmployeeServey.objects.filter(
            user=employee,
            submitted=False,
            survey__end_date__gte=timezone.now().date(),
        )
        return surveys


class SubmittedSurveyListView(ListView):
    template_name = "survey/submitted_surveys.html"
    context_object_name = "submitted_surveys"

    def get_queryset(self):
        surveys = SubmittedSurveyListView.user_submitted_surveys(
            user=self.request.user
        )
        return surveys

    @staticmethod
    def user_submitted_surveys(user):
        employee = Employee.objects.get(user=user)
        surveys = EmployeeServey.objects.filter(
            user=employee,
            submitted=True,
            survey__end_date__gte=timezone.now().date(),
        )
        return surveys


class SurveyAnswerFormView(FormView):
    """SurveyAnswerFormView handles the display and submission of survey forms."""

    template_name = "survey/survey.html"
    success_url = reverse_lazy("list_survey")
    form_class = SurveyForm

    def get_form_kwargs(self):
        """Override the default form kwargs to include the survey related to the survey ID in the URL."""
        kwargs = super(SurveyAnswerFormView, self).get_form_kwargs()
        survey_id = self.kwargs.get("survey_id")
        get_employee_survey = SurveyAnswerFormView.employee_survey(
            survey_id=survey_id
        )

        get_survey = SurveyAnswerFormView.survey(
            employee_survey=get_employee_survey
        )
        kwargs["survey"] = get_survey
        return kwargs

    def form_valid(self, form):
        """Process the form, save the answers, and update the employee survey as submitted."""
        cleaned_data = form.cleaned_data
        list_answer = []
        for field_name, value in cleaned_data.items():
            if field_name.startswith("question_"):
                question_id = int(field_name.split("_")[1])
                answer = SurveyAnswerFormView.answers(
                    question_id=question_id, value=value
                )
                list_answer.append(answer.id)

        survey_id = self.kwargs.get("survey_id")
        get_employee_survey = SurveyAnswerFormView.employee_survey(
            survey_id=survey_id
        )
        get_employee_survey.answer.set(list_answer)
        get_employee_survey.submitted = True
        get_employee_survey.save()
        return super(SurveyAnswerFormView, self).form_valid(form)

    @staticmethod
    def answers(question_id, value):
        """Create an answer object for a given question and value."""
        question = Question.objects.get(id=question_id)
        answer = Answer.objects.create(
            question=question,
            rating=value,
        )
        return answer

    @staticmethod
    def survey(employee_survey):
        """Retrieve the first survey related to a given employee survey."""
        get_survey = employee_survey.survey.all()
        return get_survey[0]

    @staticmethod
    def employee_survey(survey_id):
        """Retrieve the employee survey object related to a given survey ID."""
        return EmployeeServey.objects.filter(pk=survey_id).first()
