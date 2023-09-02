from django.views.generic import ListView, TemplateView, CreateView, FormView
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import EmployeeServey, Survey, Answer, Question
from accounts.models import Employee
from .forms import SurveyForm
from django.utils import timezone
from django.shortcuts import get_object_or_404



class SurveyView(TemplateView):
    template_name = "survey/list_survey.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        employee = Employee.objects.get(user=self.request.user)
        surveys = EmployeeServey.objects.filter(
            user=employee, submitted=False, survey__end_date__gte=timezone.now().date()
        )
        context["surveys"] = surveys
        return context
    

class SubmittedSurveyListView(ListView):
    template_name = 'survey/submitted_surveys.html'
    context_object_name = 'submitted_surveys'

    def get_queryset(self):
        employee = Employee.objects.get(user=self.request.user)
        return EmployeeServey.objects.filter(
            user=employee,
            submitted=True,
            survey__end_date__gte=timezone.now().date()
        )



class SurveyAnswerFormView(FormView):
    template_name = "survey/survey.html"
    success_url = reverse_lazy("list_survey")
    form_class = SurveyForm

    def get_form_kwargs(self):
        kwargs = super(SurveyAnswerFormView, self).get_form_kwargs()
        survey_id = self.kwargs.get("survey_id")
        get_employee_survey = EmployeeServey.objects.filter(pk=survey_id).first()
        get_survey = get_employee_survey.survey.all()
        kwargs["survey"] = get_survey[0]
        return kwargs

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        list_answer = []
        for field_name, value in cleaned_data.items():
            if field_name.startswith("question_"):
                question_id = int(field_name.split("_")[1])
                question = Question.objects.get(id=question_id)
                answer = Answer.objects.create(
                    question=question,
                    rating=value,
                )
                list_answer.append(answer.id)

        survey_id = self.kwargs.get("survey_id")
        get_employee_survey = EmployeeServey.objects.filter(pk=survey_id).first()
        get_employee_survey.answer.set(list_answer)
        # get_employee_survey.submitted = True
        get_employee_survey.save()
        return super(SurveyAnswerFormView, self).form_valid(form)
