from django.core.exceptions import ValidationError as DjValidationError
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from ..models.Lesson import Lesson
from ..models.Question import Question
from ..models.QuestionTypeChoices import QuestionTypeChoices as QTChoices
from .AnswerValueSerializer import AnswerValueSerializer


class QuestionSerializer(ModelSerializer):
    answers = AnswerValueSerializer(many=True, write_only=True)
    lesson = PrimaryKeyRelatedField(required=False,
                                    queryset=Lesson.objects.using('master'))

    class Meta:
        model = Question
        fields = (
            'id', 'body', 'question_type', 'lesson', 'answers',
        )

    def create(self, validated_data):
        question_type = validated_data.get('question_type')
        answers = validated_data.pop('answers')

        if question_type == QTChoices.FREE and len(answers) != 1:
            detail = {
                'answers': [
                    'Much values for this question_type.',
                ],
            }
            raise ValidationError(detail)

        try:
            question = Question.objects.create(**validated_data)
        except DjValidationError as ex:
            raise ValidationError(ex.error_dict)

        answers = list(
            map(lambda x: None if x.update({'question': question.id}) else x,
                answers)
        )

        serializer = AnswerValueSerializer(data=answers, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return question

    def update(self, instance, validated_data):
        if 'answers' in validated_data:
            del validated_data['answers']

        if 'lesson' in validated_data:
            del validated_data['lesson']

        return super().update(instance, validated_data)
