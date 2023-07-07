import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphene import relay
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from courses.models.UserCourse import UserCourse

from ..models.Lesson import Lesson
from ..tasks.UpdateUserCourseLastViewTask import \
    update_user_course_last_view_task
from .PrivateLessonType import PrivateLessonType


class LessonType(PrivateLessonType):
    body = graphene.String()

    class Meta:
        model = PrivateLessonType._meta.model
        interfaces = (relay.Node,)
        fields = (
            'id', 'serial_number', 'title', 'description', 'lesson_type',
            'time_limit', 'count_questions', 'is_completed',
        )

    @classmethod
    @login_required
    def get_node(cls, info, id):
        user = info.context.user
        lesson = Lesson.objects.get(pk=id)

        user_courses = UserCourse.objects.filter(**{
            'course_id': lesson.course_id,
            'user': user,
        }).first()

        if not user_courses:
            raise GraphQLError('You do not have access to this lesson.')

        update_user_course_last_view_task.apply_async(kwargs={
            'user_course_id': user_courses.id,
        })

        return lesson

    def resolve_body(self, info):
        try:
            return self.lesson_body.body
        except ObjectDoesNotExist:
            return None


class LessonQuery(graphene.ObjectType):
    lesson = relay.Node.Field(LessonType)
