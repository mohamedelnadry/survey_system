from django import forms
from .models import Question, Answer, EmployeeServey
from django.core.validators import MinValueValidator, MaxValueValidator


class SurveyForm(forms.ModelForm):
    class Meta:
        model = EmployeeServey
        fields = []

    def __init__(self, *args, **kwargs):
        survey = kwargs.pop('survey', None)
        super(SurveyForm, self).__init__(*args, **kwargs)
        
        if survey:
            questions = survey.questions.all()
            for question in questions:
                field_name = f'{question.id}'
                self.fields[field_name] = forms.FloatField(
                    label=str(question),
                    validators=[MinValueValidator(0), MaxValueValidator(10)],
                )
