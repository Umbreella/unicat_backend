from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models.Lesson import Lesson
from ..models.LessonTypeChoices import LessonTypeChoices
from ..models.UserLesson import UserLesson


class LessonCompleteSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField(write_only=True)

    def save(self, **kwargs):
        user = self.context.get('user')
        lesson_id = self.validated_data.get('lesson_id')

        lesson = Lesson.objects.get(pk=lesson_id)

        if lesson.lesson_type != LessonTypeChoices.THEORY.value:
            detail = {
                'lesson_id': [
                    'You can not complete lesson this type.',
                ],
            }
            raise ValidationError(detail)

        user_lesson, is_created = UserLesson.objects.get_or_create(**{
            'lesson': lesson,
            'user': user,
        })

        if is_created:
            user_lesson.completed_at = timezone.now()
            user_lesson.save()

        return user_lesson
