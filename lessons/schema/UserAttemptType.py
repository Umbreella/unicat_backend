import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from graphene import String, relay
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from courses.models.UserCourse import UserCourse

from ..models.Lesson import Lesson
from ..models.LessonTypeChoices import LessonTypeChoices
from ..models.UserAttempt import UserAttempt
from ..models.UserLesson import UserLesson


class UserAttemptType(DjangoObjectType):
    duration = graphene.Int()

    class Meta:
        model = UserAttempt
        interfaces = (relay.Node,)
        fields = (
            'id', 'time_end', 'count_true_answer',
        )

    def resolve_duration(self, info):
        return int((self.time_end - self.time_start).total_seconds())


class UserAttemptTypeConnection(relay.Connection):
    class Meta:
        node = UserAttemptType


class UserAttemptQuery(graphene.ObjectType):
    my_attempts = relay.ConnectionField(UserAttemptTypeConnection,
                                        lesson_id=String(required=True))

    @login_required
    def resolve_my_attempts(root, info, *args, **kwargs):
        user = info.context.user
        type_, lesson_id = from_global_id(kwargs.get('lesson_id'))

        if type_ != 'LessonType':
            raise GraphQLError('lessonId: not valid value.')

        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except ObjectDoesNotExist:
            raise GraphQLError('Lesson with this id is not found.')

        has_access = UserCourse.objects.filter(**{
            'course_id': lesson.course_id,
            'user': user,
        }).exists()

        if not has_access:
            raise GraphQLError('You do not have access to this lesson.')

        if lesson.lesson_type != LessonTypeChoices.TEST.value:
            raise GraphQLError('Lesson this type has no attempts.')

        user_lesson, is_created = UserLesson.objects.get_or_create(**{
            'lesson': lesson,
            'user': user,
        })

        queryset = UserAttempt.objects.using('master').filter(**{
            'user_lesson': user_lesson,
            'time_end__lte': timezone.now(),
        }).order_by('-time_end')

        return queryset
