from django import forms
from django.contrib.auth.models import User
from .models import Employee
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):  
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise ValidationError("Invalid username or password")

        return cleaned_data



class EmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Employee
        fields = ['job_title', 'department']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters.")
        return password

    def save(self, commit=True):
        employee = super().save(commit=False)
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()

        employee.user = user

        if commit:
            employee.save()

        return employee
