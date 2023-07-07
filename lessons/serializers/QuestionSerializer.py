from rest_framework.serializers import ModelSerializer

from ..models.Question import Question


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id', 'body', 'question_type', 'lesson',
        )
