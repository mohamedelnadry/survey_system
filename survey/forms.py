"""Survey App Forms."""
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import Answer, EmployeeServey, Question


class SurveyForm(forms.ModelForm):
    """
    Form for EmployeeSurvey model.
    """

    class Meta:
        model = EmployeeServey
        fields = []

    def __init__(self, *args, **kwargs):
        survey = kwargs.pop("survey", None)
        super(SurveyForm, self).__init__(*args, **kwargs)

        if survey:
            questions = survey.questions.all()
            for question in questions:
                field_name = f"question_{question.id}"
                self.fields[field_name] = forms.FloatField(
                    label=str(question),
                    validators=[MinValueValidator(0), MaxValueValidator(10)],
                )
