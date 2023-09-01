from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Employee
        fields = ['username', 'password', 'job_title', 'department']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
