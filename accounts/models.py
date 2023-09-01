from django import forms
from django.contrib.auth.models import User
from .models import Employee

class EmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Employee
        fields = ['job_title', 'department']

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
