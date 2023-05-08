import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphene import relay
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from courses.models.UserCourse import UserCourse

from ..models.Lesson import Lesson


class LessonType(DjangoObjectType):
    serial_number = graphene.String()
    body = graphene.String()
    lesson_type = graphene.String()
    is_completed = graphene.Boolean()

    class Meta:
        model = Lesson
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

        has_access = UserCourse.objects.filter(**{
            'course_id': lesson.course_id,
            'user': user,
        }).exists()

        if not has_access:
            raise GraphQLError('You do not have access to this lesson.')

        return lesson

    def resolve_serial_number(self, info):
        parent = self.parent
        result = ''

        if parent:
            result += f'{parent.serial_number}.'

        return f'{result}{self.serial_number}'

    def resolve_body(self, info):
        try:
            return self.lesson_body.body
        except ObjectDoesNotExist:
            return None

    def resolve_lesson_type(self, info):
        return self.get_lesson_type_display()

    @login_required
    def resolve_is_completed(self, info):
        user = info.context.user

        try:
            return bool(self.progress.get(user=user).completed_at)
        except ObjectDoesNotExist:
            return False


class LessonConnection(relay.Connection):
    class Meta:
        node = LessonType


class LessonQuery(graphene.ObjectType):
    lesson = relay.Node.Field(LessonType)
