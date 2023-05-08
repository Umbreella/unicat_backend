from rest_framework.serializers import ModelSerializer

from ..models.Lesson import Lesson


class ListLessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id', 'title', 'lesson_type', 'serial_number', 'parent',
        )
