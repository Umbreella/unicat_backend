import graphene
from graphene_django import DjangoObjectType

from ..models.Lesson import Lesson
from ..nodes.LessonTypeNode import LessonTypeNode


class PublicLessonType(DjangoObjectType):
    serial_number = graphene.String()
    lesson_type = graphene.String()

    class Meta:
        model = Lesson
        interfaces = (LessonTypeNode,)
        fields = (
            'id', 'serial_number', 'title', 'description', 'lesson_type',
        )

    def resolve_serial_number(self, info):
        parent = f'{self.parent.serial_number}.' if self.parent else ''

        return f'{parent}{self.serial_number}.'

    def resolve_lesson_type(self, info):
        return self.get_lesson_type_display()
