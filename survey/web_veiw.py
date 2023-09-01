from django.views.generic import ListView, TemplateView, CreateView
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import EmployeeServey, Employee
from .forms import SurveyForm
from django.utils import timezone



class SurveyView(TemplateView):
    template_name = 'survey/list_survey.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        employee = Employee.objects.get(user=self.request.user)
        surveys = EmployeeServey.objects.filter(
            user=employee,
            submitted=False,
            survey__end_date__gte=timezone.now().date()
        )
        context['surveys'] = surveys
        return context



class SurveyAnswerFormView(CreateView):
    form_class = SurveyForm
    template_name = 'survey/survey.html'
    success_url = reverse_lazy('temp_register')  
