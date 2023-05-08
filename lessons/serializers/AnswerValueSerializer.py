from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from ..models.AnswerValue import AnswerValue
from ..models.Question import Question


class AnswerValueSerializer(ModelSerializer):
    question = PrimaryKeyRelatedField(required=False,
                                      queryset=Question.objects.using('master')
                                      )

    class Meta:
        model = AnswerValue
        fields = (
            'id', 'question', 'value', 'is_true',
        )
