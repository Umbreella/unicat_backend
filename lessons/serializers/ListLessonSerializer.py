from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..models.Lesson import Lesson


class ListLessonSerializer(ModelSerializer):
    serial_number = SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            'id', 'title', 'lesson_type', 'serial_number', 'parent',
        )

    def get_serial_number(self, obj):
        parent = f'{obj.parent.serial_number}.' if obj.parent else ''

        return f'{parent}{obj.serial_number}.'
