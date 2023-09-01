from rest_framework import serializers
from .models import Survey, Question, Answer, EmployeeServey

from rest_framework.exceptions import ValidationError


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["question", "rating"]


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ["id", "name", "questions", "start_date", "end_date"]


class EmployeeSerializer(serializers.ModelSerializer):
    survey = SurveySerializer(many=True)
    answer = AnswerSerializer(many=True)

    class Meta:
        model = EmployeeServey
        fields = ["id", "user", "survey", "answer"]

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        if instance['answer']==[]:
            instance.pop('answer')
        return instance



class EmployeeSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeServey
        fields = ["id", "user", "survey", "answer"]

    def create(self, validated_data):
        validated_data["submitted"] = True
        instance = super(EmployeeSubmitSerializer, self).create(validated_data)
        return instance
