from django import forms
from .models import EmployeeServey


class SurveyForm(forms.ModelForm):
    
    class Meta:
        model = EmployeeServey
        fields = ['answer']