import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphene import String
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from courses.models.UserCourse import UserCourse
from courses.schema.CourseType import CourseType
from unicat.graphql.functions import get_id_from_value, get_value_from_model_id

from ..models.Lesson import Lesson
from ..models.LessonTypeChoices import LessonTypeChoices
from .LessonType import LessonType


class ParentLessonType(DjangoObjectType):
    id = graphene.String()
    lesson_type = graphene.String()
    is_completed = graphene.Boolean()
    children = graphene.List(LessonType)

    class Meta:
        model = Lesson
        fields = (
            'serial_number', 'title', 'description',
        )

    def resolve_id(self, info):
        return get_value_from_model_id(LessonType, self.id)

    def resolve_lesson_type(self, info):
        return self.get_lesson_type_display()

    @login_required
    def resolve_is_completed(self, info):
        user = info.context.user

        try:
            return bool(self.progress.get(user=user).completed_at)
        except ObjectDoesNotExist:
            return False

    def resolve_children(self, info):
        path = info.path
        lesson_filter = {}

        while path is not None:
            if path.key == 'lessonsByCourse':
                lesson_filter.update({
                    'lesson_type__in': [
                        LessonTypeChoices.THEORY.value,
                        LessonTypeChoices.THEME.value,
                    ],
                })
                break
            path = path.prev

        return self.children.filter(
            **lesson_filter,
        ).order_by('serial_number')


class ParentLessonQuery(graphene.ObjectType):
    lessons_by_course = graphene.List(ParentLessonType,
                                      course_id=String(required=True))

    lessons_with_progress = graphene.List(ParentLessonType,
                                          course_id=String(required=True))

    def resolve_lessons_by_course(root, info, *args, **kwargs):
        course_id_str = kwargs.get('course_id')

        try:
            course_id = get_id_from_value(CourseType, course_id_str)
        except Exception as ex:
            raise GraphQLError(f'courseId: {ex}')

        lesson_type_filter = [
            LessonTypeChoices.THEORY.value,
            LessonTypeChoices.THEME.value,
        ]

        return Lesson.objects.filter(**{
            'course_id': course_id,
            'parent': None,
            'lesson_type__in': lesson_type_filter,
        }).order_by(
            'serial_number',
        )

    @login_required
    def resolve_lessons_with_progress(root, info, *args, **kwargs):
        user = info.context.user
        course_id_str = kwargs.get('course_id')

        try:
            course_id = get_id_from_value(CourseType, course_id_str)
        except Exception as ex:
            raise GraphQLError(f'courseId: {ex}')

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
