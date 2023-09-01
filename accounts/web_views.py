from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.contrib.auth import login
from .forms import EmployeeForm, LoginForm
from django.contrib.auth import login


class Register(CreateView):
    form_class = EmployeeForm
    success_url = reverse_lazy('temp_register')  
    template_name = 'accounts/register.html'


class LoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('temp_register')  

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            return redirect('/')
        return render(request, self.template_name, context={'form': form, 'message': 'Login failed!'})