import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from graphene import String, relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from courses.models.UserCourse import UserCourse
from unicat.graphql.functions import get_id_from_value

from ..filtersets.UserAttemptFilterSet import UserAttemptFilterSet
from ..models.Lesson import Lesson
from ..models.LessonTypeChoices import LessonTypeChoices
from ..models.UserAttempt import UserAttempt
from ..models.UserLesson import UserLesson
from .LessonType import LessonType


class UserAttemptType(DjangoObjectType):
    duration = graphene.Int()

    class Meta:
        model = UserAttempt
        interfaces = (relay.Node,)
        fields = (
            'id', 'time_end', 'count_true_answer',
        )

    def resolve_duration(self, info):
        duration = self.time_end - self.time_start

        return duration.total_seconds()


class UserAttemptQuery(graphene.ObjectType):
    my_attempts = DjangoFilterConnectionField(**{
        'type_': UserAttemptType,
        'filterset_class': UserAttemptFilterSet,
        'lesson_id': String(required=True),
    })

    @login_required
    def resolve_my_attempts(root, info, *args, **kwargs):
        user = info.context.user
        lesson_id_b64 = kwargs.get('lesson_id')

        try:
            lesson_id = get_id_from_value(LessonType, lesson_id_b64)
        except Exception as ex:
            raise GraphQLError(f'lesson_id: {ex}')

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

        queryset = UserAttempt.objects.filter(**{
            'user_lesson': user_lesson,
            'time_end__lte': timezone.now(),
        }).order_by('-time_end')

        return queryset
