from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import EmployeeForm
from .models import Employee


class Register(CreateView):
    form_class = EmployeeForm
    success_url = reverse_lazy('temp_register')  
    template_name = 'accounts/register.html'

