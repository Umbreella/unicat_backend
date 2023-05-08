from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from unicat.graphql.functions import get_value_from_model_id

from ..models.Lesson import Lesson
from ..models.LessonTypeChoices import LessonTypeChoices
from ..models.UserAttempt import UserAttempt
from ..models.UserLesson import UserLesson


class UserAttemptSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    time_end = serializers.DateTimeField(read_only=True)
    count_answered_questions = serializers.SerializerMethodField()
    lesson_id = serializers.IntegerField(write_only=True)

    def get_id(self, obj):
        self.__attempt_global_id = get_value_from_model_id('UserAttemptType',
                                                           obj.id)
        return self.__attempt_global_id

    def get_count_answered_questions(self, obj):
        cache_key = f'{self.__attempt_global_id}_answered_questions'
        answered_questions_ids = cache.get(cache_key, [])

        return len(answered_questions_ids)

    def validate(self, attrs):
        lesson_id = attrs.get('lesson_id')
        self._lesson = Lesson.objects.get(pk=lesson_id)

        if self._lesson.lesson_type != LessonTypeChoices.TEST.value:
            detail = {
                'lesson_id': [
                    'You can not create attempt for this type lesson.',
                ],
            }
            raise ValidationError(detail)

        return attrs

    def create(self, validated_data):
        user = self.context.get('user')

        user_lesson, is_created = UserLesson.objects.get_or_create(**{
            'lesson': self._lesson,
            'user': user,
        })

        user_attempt = UserAttempt.objects.create(**{
            'user_lesson': user_lesson,
        })

        return user_attempt
