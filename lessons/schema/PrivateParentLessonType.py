import graphene
from graphene import String
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from courses.models.UserCourse import UserCourse
from courses.schema.CourseType import CourseType

from ..models.Lesson import Lesson
from .PrivateLessonType import PrivateLessonType
from .PublicParentLessonType import PublicParentLessonType


class PrivateParentLessonType(PrivateLessonType):
    children = graphene.List(PrivateLessonType)

    class Meta:
        model = PublicParentLessonType._meta.model
        interfaces = PublicParentLessonType._meta.interfaces
        fields = tuple(PublicParentLessonType._meta.fields)

    def resolve_children(self, info):
        return info.context.loaders.private_children_loader.load(self.id)


class PrivateParentLessonQuery(graphene.ObjectType):
    lessons_with_progress = graphene.List(PrivateParentLessonType,
                                          course_id=String(required=True))

    @login_required
    def resolve_lessons_with_progress(root, info, *args, **kwargs):
        user = info.context.user

        type_, course_id = from_global_id(kwargs.get('course_id'))

        if type_ != CourseType.__name__:
            raise GraphQLError('courseId: not valid value.')

        has_access = UserCourse.objects.filter(**{
            'course_id': course_id,
            'user': user,
        }).exists()

        if not has_access:
            raise GraphQLError('You don`t have access to this course.')

        return Lesson.objects.filter(**{
            'course_id': course_id,
            'parent': None,
        }).order_by(
            'serial_number',
        )
