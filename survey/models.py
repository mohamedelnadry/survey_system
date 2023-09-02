"""Survey App Models."""
from django.db import models
from core.models import BaseModel
from accounts.models import Employee
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

# Enum for question types
QUESTION_TYPE_CHOICES = [
    ("general", "General"),
    ("followers", "Followers"),
    ("reversed", "Reversed"),
]


class Question(BaseModel):
    """Model for survey questions."""
    text = models.TextField()

    def __str__(self):
        return self.text


class Survey(models.Model):
    """Model for a survey."""
    name = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question, related_name="questions")
    type_employee = models.CharField(
        max_length=15, choices=QUESTION_TYPE_CHOICES, default="general"
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("survey-detail", kwargs={"id": self.pk})


class Answer(BaseModel):
    """Model for answers to survey questions."""
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )
    rating = models.FloatField()

    def __str__(self):
        return self.question.text


class EmployeeServey(BaseModel):
    """Model for storing surveys related to an employee."""
    user = models.ForeignKey(
        Employee, related_name="employee_survey", on_delete=models.CASCADE
    )
    survey = models.ManyToManyField(Survey, related_name="survey")
    answer = models.ManyToManyField(
        Answer, related_name="asnwers", blank=True
    )
    submitted = models.BooleanField(default=False)

    @receiver(post_save, sender=Survey)
    def create_employee_survey(sender, instance, **kwargs):
        """Signal to create an EmployeeSurvey instance based on the type of employee."""

        # General type of survey
        if instance.type_employee == "general":
            """Assuming Employee has a field `is_admin` to check for admin status."""
            for employee in Employee.objects.all():
                employee_survey = EmployeeServey.objects.create(user=employee)
                employee_survey.survey.add(instance)

         # Followers type of survey
        elif instance.type_employee == "followers":
            """Assuming immediate parents are to be considered for 'followers'."""
            parents = Employee.objects.exclude(children__isnull=True)
            for parent in parents:
                employee_survey = EmployeeServey.objects.create(user=parent)
                employee_survey.survey.add(instance)
                
        # Reversed type of survey
        elif instance.type_employee == "reversed":
            """For the reversed case, find all employees who are parents."""
            for employee in Employee.objects.exclude(parent__isnull=True):
                employee_survey = EmployeeServey.objects.create(user=employee)
                employee_survey.survey.add(instance)

    def __str__(self):
        return self.user.user.username
