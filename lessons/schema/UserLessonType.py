from datetime import timedelta

import graphene
from django.db.models import Count
from django.utils import timezone
from graphql_jwt.decorators import login_required

from ..models.LessonTypeChoices import LessonTypeChoices
from ..models.UserLesson import UserLesson


class UserLessonType(graphene.ObjectType):
    completed_at = graphene.DateTime()
    count_lesson = graphene.Int()


class UserLessonQuery(graphene.ObjectType):
    my_lesson_history = graphene.List(UserLessonType)

    @login_required
    def resolve_my_lesson_history(root, info, **kwargs):
        data = list(UserLesson.objects.filter(**{
            'user': info.context.user,
            'completed_at__gte': timezone.now() - timedelta(days=6),
        }).exclude(**{
            'lesson__lesson_type': LessonTypeChoices.THEME,
        }).annotate(**{
            'count_lesson': Count('completed_at'),
        }).values(
            'completed_at', 'count_lesson',
        ).order_by('-completed_at'))

        history = []
        for i in range(7):
            current_date = (timezone.now() - timedelta(days=6 - i)).date()

            if data and data[0]['completed_at'] == current_date:
                history.append(data.pop(0))
            else:
                history.append({
                    'completed_at': current_date,
                    'count_lesson': 0,
                })

        return history
