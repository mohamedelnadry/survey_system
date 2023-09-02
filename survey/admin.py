"""Survey App Admin."""
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Survey, Question, Answer, EmployeeServey

class SurveyForm(forms.ModelForm):
    """Form for validating Survey instance in admin panel."""
    
    class Meta:
        model = Survey
        fields = '__all__'

    def clean(self):
        """Validate start and end date fields."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date and start_date and end_date <= start_date:
            raise ValidationError("End date should be after start date")


class QuestionAdmin(admin.ModelAdmin):
    """Admin class for Question model."""
    search_fields = ['text']


class SurveyAdmin(admin.ModelAdmin):
    """Admin class for Survey model."""
    form = SurveyForm
    list_display = ['name', 'start_date', 'end_date']
    search_fields = ['name']


class EmployeeServeyAdmin(admin.ModelAdmin):
    """Admin class for EmployeeServey model."""

    def get_survey_names(self, obj):
        """Get comma-separated list of survey names associated with an employee."""
        return ", ".join([str(survey.name) for survey in obj.survey.all()])
    
    get_survey_names.short_description = "Surveys"
    
    list_display = ['user', 'get_survey_names', 'submitted']
    search_fields = ['survey__name']


# Registering models for the admin panel
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(EmployeeServey, EmployeeServeyAdmin)
