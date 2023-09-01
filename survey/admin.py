from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Survey, Question, Answer, EmployeeServey

from django.contrib import admin
from django import forms
from .models import Survey, Question, Answer

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date and start_date and end_date <= start_date:
            raise forms.ValidationError("End date should be after start date")

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['text']

class SurveyAdmin(admin.ModelAdmin):
    form = SurveyForm
    list_display = ['name', 'start_date', 'end_date']
    search_fields = ['name']

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)

admin.site.register(Answer)
admin.site.register(EmployeeServey)
