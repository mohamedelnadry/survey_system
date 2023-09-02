"""Accounts App Serializer."""
from rest_framework import serializers
from .models import Survey, Question, Answer, EmployeeServey

from rest_framework.exceptions import ValidationError


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model."""
    class Meta:
        model = Question
        fields = ["id", "text"]


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for Answer model."""
    class Meta:
        model = Answer
        fields = ["question", "rating"]


class SurveySerializer(serializers.ModelSerializer):
    """Serializer for Survey model with nested questions."""
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ["id", "name", "questions", "start_date", "end_date"]


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeServey model with nested survey and answer."""
    survey = SurveySerializer(many=True)
    answer = AnswerSerializer(many=True)

    class Meta:
        model = EmployeeServey
        fields = ["id", "user", "survey", "answer"]

    def to_representation(self, instance):
        """Modify the serialized output."""
        instance = super().to_representation(instance)
        if instance['answer']==[]:
            instance.pop('answer')
        return instance