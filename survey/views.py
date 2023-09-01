from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, views
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound
from .models import Survey, Question, Answer, EmployeeServey
from accounts.models import Employee
from .serializers import (
    SurveySerializer,
    QuestionSerializer,
    EmployeeSerializer,
    EmployeeSubmitSerializer,
)
from django.utils import timezone



class SurveyView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        employee = Employee.objects.get(user=self.request.user)
        surveys = EmployeeServey.objects.filter(user=employee, submitted=False, survey__end_date__gte=timezone.now().date())
        return surveys


class SubmitedSurveyView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        employee = Employee.objects.get(user=self.request.user)
        surveys = EmployeeServey.objects.filter(user=employee, submitted=True, survey__end_date__gte=timezone.now().date())
        return surveys


class SurveyAnswer(views.APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        employee = Employee.objects.get(user=self.request.user)
        survey = request.data.get("survey")
        answers = request.data.pop("answers")
        request.data["user"] = employee.id
        try:
            get_survey = Survey.objects.get(id=survey[0])
            if get_survey.end_date < timezone.now().date():
                return Response(
                {"message": "Survey Not Found"}, status=status.HTTP_204_NO_CONTENT
            )
            questions = get_survey.questions.all()
        except e:
            print(f"survey error {e}")

        if len(answers) == len(questions):
            answer_list = []
            for i in questions:
                for j in answers:
                    if i.id == j["question_id"]:
                        answer = Answer.objects.create(question=i, rating=j["rating"])
                        answer_list.append(answer.id)

        request.data["user"] = employee.id
        request.data["answer"] = answer_list
        serializer = EmployeeSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            {"message": "Survey answers submitted successfully"},
            status=status.HTTP_201_CREATED,
        )


class DetailSurveyView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        try:
            employee = Employee.objects.get(user=self.request.user)
        except Employee.DoesNotExist:
            raise NotFound("Employee not found")

        pk = self.kwargs.get("pk")
        survey = Survey.objects.filter(id=pk).first()

        if not survey or survey.end_date < timezone.now().date():
            raise NotFound("Survey not found")

        employee_survey = EmployeeServey.objects.filter(
            survey=survey, user=employee
        ).exists()

        if not employee_survey:
            raise NotFound("Employee doesn't have access to this survey")

        return survey.questions.all()
