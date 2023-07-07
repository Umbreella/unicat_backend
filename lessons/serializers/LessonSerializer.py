from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField, ModelSerializer

from ..models.Lesson import Lesson
from ..models.LessonBody import LessonBody
from ..models.LessonTypeChoices import LessonTypeChoices as LTChoices


class LessonSerializer(ModelSerializer):
    body = CharField(source='lesson_body.body', required=False)

    class Meta:
        model = Lesson
        fields = (
            'id', 'course', 'serial_number', 'title', 'lesson_type',
            'description', 'body', 'parent',
        )

    def __init__(self, *args, **kwargs):
        self._lesson_body = None

        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        if 'lesson_body' in attrs:
            self._lesson_body = attrs.pop('lesson_body')

        lesson_type = attrs.get('lesson_type')
        parent = attrs.get('parent')

        if lesson_type == LTChoices.THEORY and not self._lesson_body:
            detail = {
                'body': [
                    'Required field for this lesson_type.',
                ],
            }
            raise ValidationError(detail)

        if lesson_type == LTChoices.THEME and parent is not None:
            detail = {
                'parent': [
                    'Theme can`t have parent_lesson.',
                ],
            }
            raise ValidationError(detail)

        return attrs

    def create(self, validated_data):
        lesson = Lesson.objects.create(**validated_data)

        if lesson.lesson_type == LTChoices.THEORY:
            LessonBody.objects.create(**{
                **self._lesson_body,
                'lesson': lesson,
            })

        return lesson

    def update(self, instance, validated_data):
        if instance.lesson_type == LTChoices.THEORY and self._lesson_body:
            instance.lesson_body.body = self._lesson_body['body']
            instance.lesson_body.save()

        return super().update(instance, validated_data)
