import graphene
from graphene import String
from graphql import GraphQLError
from graphql_relay import from_global_id

from courses.schema.CourseType import CourseType

from ..models.Lesson import Lesson
from ..models.LessonTypeChoices import LessonTypeChoices
from .PublicLessonType import PublicLessonType


class PublicParentLessonType(PublicLessonType):
    children = graphene.List(PublicLessonType)

    class Meta:
        model = PublicLessonType._meta.model
        interfaces = PublicLessonType._meta.interfaces
        fields = (
            'id', 'serial_number', 'title', 'description',
        )

    def resolve_children(self, info):
        return info.context.loaders.public_children_loader.load(self.id)


class PublicParentLessonQuery(graphene.ObjectType):
    lessons_by_course = graphene.List(PublicParentLessonType,
                                      course_id=String(required=True))

    def resolve_lessons_by_course(root, info, *args, **kwargs):
        type_, course_id = from_global_id(kwargs.get('course_id'))

        if type_ != CourseType.__name__:
            raise GraphQLError('courseId: not valid value.')

        return Lesson.objects.filter(**{
            'course_id': course_id,
            'parent': None,
            'lesson_type__in': [
                LessonTypeChoices.THEORY.value,
                LessonTypeChoices.THEME.value,
            ],
        }).order_by(
            'serial_number',
        )
