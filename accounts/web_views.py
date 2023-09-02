"""Accounts App Web_Views."""
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.contrib.auth import login
from .forms import EmployeeForm, LoginForm

class Register(CreateView):
    """
    View for user registration.
    """
    
    form_class = EmployeeForm
    success_url = reverse_lazy('login')  
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/listsurvey')
        return super().get(request, *args, **kwargs)

class LoginView(View):
    """
    View for user login.
    """
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('list_survey')  

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/listsurvey')
        
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            return redirect('/listsurvey')
        
        return render(request, self.template_name, context={'form': form, 'message': 'Login failed!'})
