"""Survey App Views."""
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, status, views
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import Employee

from .models import Answer, EmployeeServey, Question, Survey
from .serializers import (
    EmployeeSerializer,
    QuestionSerializer,
    SurveySerializer,
)


class SurveyView(generics.ListAPIView):
    """List all surveys available for an employee."""

    authentication_classes = [JWTAuthentication]
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        surveys = SurveyView.list_survey(user=self.request.user)
        return surveys

    @staticmethod
    def list_survey(user):
        """Retrieve all active surveys for a given employee."""
        employee = Employee.objects.get(user=user)
        surveys = EmployeeServey.objects.filter(
            user=employee,
            submitted=False,
            survey__end_date__gte=timezone.now().date(),
        )
        return surveys


class SubmitedSurveyView(generics.ListAPIView):
    """List all submitted surveys for an employee."""

    authentication_classes = [JWTAuthentication]
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return SurveyView.list_submitted_survey(user=self.request.user)

    @staticmethod
    def list_submitted_survey(user):
        """Retrieve all submitted surveys for a given employee."""
        employee = Employee.objects.get(user=user)
        surveys = EmployeeServey.objects.filter(
            user=employee,
            submitted=True,
            survey__end_date__gte=timezone.now().date(),
        )
        return surveys


class SurveyAnswer(views.APIView):
    """Class for submitting answers to a survey."""

    authentication_classes = [JWTAuthentication]

    def post(self, request):
        """
        Handle POST requests to submit survey answers.

        Args:
            request (Request): The request object containing survey and answers data.

        Returns:
            Response: A response object indicating the success or failure of the operation.
        """
        employee = SurveyAnswer.get_employee(user=self.request.user)
        survey = request.data.get("survey")
        answers = request.data.pop("answers")
        check_employee_survey = SurveyAnswer.check_employee_survey(
            employee=employee, survey_id=survey[0]
        )
        if check_employee_survey:
            return Response(
                {"message": "This survey submited before"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        get_employee_survey = SurveyAnswer.get_employee_survey(
            employee=employee, survey_id=survey[0]
        )
        questions = SurveyAnswer.get_questions(survey)
        if not questions:
            return Response(
                {"message": "Survey Not Found"},
                status=status.HTTP_204_NO_CONTENT,
            )
        answers = SurveyAnswer.create_answer(
            answers=answers, questions=questions
        )
        if not answers:
            return Response(
                {"message": "Check questions and answers"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        get_employee_survey.answer.set(answers)
        get_employee_survey.submitted = True
        get_employee_survey.save()

        return Response(
            {"message": "Survey answers submitted successfully"},
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def get_employee_survey(employee, survey_id):
        """Retrieve the EmployeeServey object for a given employee and survey ID."""
        survey_employee = EmployeeServey.objects.filter(
            user=employee, survey=survey_id, submitted=False
        ).first()
        return survey_employee

    @staticmethod
    def check_employee_survey(employee, survey_id):
        """Check if an employee has already submitted a survey."""
        try:
            get_survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            return False

        survey_employee = EmployeeServey.objects.filter(
            user=employee, submitted=True, survey__in=[get_survey.id]
        ).exists()
        return survey_employee

    @staticmethod
    def get_employee(user):
        """Retrieve the Employee object for a given user."""
        return Employee.objects.get(user=user)

    @staticmethod
    def create_answer(answers, questions):
        """
        Create Answer objects by associating them with corresponding questions.
        """
        if len(answers) != len(questions):
            return None

        answer_list = []

        for question in questions:
            for answer_data in answers:
                if question.id == answer_data["question_id"]:
                    answer = Answer.objects.create(
                        question=question, rating=answer_data["rating"]
                    )
                    answer_list.append(answer.id)

        return answer_list

    @staticmethod
    def get_questions(survey):
        """Retrieve all questions for a given survey ID."""
        try:
            get_survey = Survey.objects.get(id=survey[0])
            if get_survey.end_date < timezone.now().date():
                return None
            questions = get_survey.questions.all()
            return questions
        except:
            return None


class DetailSurveyView(generics.ListAPIView):
    """List all questions for a given survey."""

    authentication_classes = [JWTAuthentication]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        """Overriding the get_queryset method to filter questions based on the authenticated user and survey ID."""
        employee = DetailSurveyView.get_employee(user=self.request.user)

        pk = self.kwargs.get("pk")
        survey = DetailSurveyView.get_questions(survey=pk, employee=employee)

        return survey

    @staticmethod
    def get_employee(user):
        """Retrieve the Employee object associated with a given user."""
        return Employee.objects.get(user=user)

    @staticmethod
    def get_questions(survey, employee):
        """Fetch all questions for a given survey ID and employee."""
        try:
            get_survey = Survey.objects.get(id=survey)
            if get_survey.end_date < timezone.now().date():
                return None

            survey_employee = EmployeeServey.objects.filter(
                user=employee, survey=get_survey, submitted=False
            )
            if not survey_employee:
                return None
            questions = get_survey.questions.all()
            return questions
        except Exception as e:
            print(e)
            return None
