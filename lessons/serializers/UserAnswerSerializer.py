from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError as DjValidationError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from unicat.graphql.functions import get_id_from_value, get_value_from_model_id

from ..models.Question import Question
from ..models.QuestionTypeChoices import QuestionTypeChoices
from ..models.UserAnswer import UserAnswer
from ..models.UserAttempt import UserAttempt
from ..schema.QuestionType import QuestionType
from ..schema.UserAttemptType import UserAttemptType


class UserAnswerSerializer(serializers.Serializer):
    attempt_id = serializers.CharField(max_length=64, write_only=True)
    question_id = serializers.CharField(max_length=64, write_only=True)
    answer = serializers.ListField(child=serializers.CharField(max_length=64),
                                   allow_empty=False, max_length=10,
                                   write_only=True)

    def validate(self, attrs):
        attempt_id_b64 = attrs['attempt_id']
        question_id_b64 = attrs['question_id']

        try:
            attempt_id = get_id_from_value(UserAttemptType, attempt_id_b64)
        except Exception as ex:
            raise ValidationError({'attempt_id': [ex]})

        try:
            self._user_attempt = UserAttempt.objects.select_related(
                'user_lesson'
            ).get(pk=attempt_id)
        except ObjectDoesNotExist:
            detail = {
                'attempt_id': [
                    'This attempt does not exist.',
                ],
            }
            raise ValidationError(detail)

        try:
            question_id = get_id_from_value(QuestionType, question_id_b64)
        except Exception as ex:
            raise ValidationError({'question_id': [ex]})

        try:
            self._question = Question.objects.get(pk=question_id)
        except ObjectDoesNotExist:
            detail = {
                'question_id': [
                    'This question does not exist.',
                ],
            }
            raise ValidationError(detail)

        return {
            'answer': attrs['answer'],
        }

    def create(self, validated_data):
        user_answers = validated_data.get('answer')
        user = self.context.get('user')

        user_attempt = self._user_attempt
        if user.id != user_attempt.user_lesson.user_id:
            detail = {
                'attempt_id': [
                    'You do not have access to this attempt.'
                ],
            }
            raise PermissionDenied(detail)

        time_end = user_attempt.time_end
        if time_end:
            if timezone.now() > time_end:
                detail = {
                    'attempt_id': [
                        (
                            'The time for this attempt is over, the answers '
                            'are no longer counted.'
                        ),
                    ],
                }
                raise PermissionDenied(detail)

        question = self._question
        question_type = question.question_type

        true_answers = question.answers.filter(**{
            'is_true': True,
        })

        if question_type == QuestionTypeChoices.FREE:
            if len(user_answers) != 1:
                detail = {
                    'answer': [
                        'For this question you cant give more than 1 answer.',
                    ],
                }
                raise ValidationError(detail)

            true_answers = [answer.value for answer in true_answers]
        else:
            true_answers_id = [answer.id for answer in true_answers]
            get_decoded_id = get_value_from_model_id

            true_answers = [
                get_decoded_id('AnswerValueType', id) for id in true_answers_id
            ]

        user_answer_is_true = sorted(true_answers) == sorted(user_answers)

        try:
            user_answer = UserAnswer.objects.create(**{
                'user_attempt': user_attempt,
                'question': question,
                'is_true': user_answer_is_true,
            })
        except DjValidationError:
            detail = {
                'question_id': [
                    (
                        'This question has already been answered in the '
                        'specified attempt.'
                    ),
                ],
            }
            raise ValidationError(detail)

        return user_answer
