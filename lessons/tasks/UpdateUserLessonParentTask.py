from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction
from django.utils import timezone

from ..models.Lesson import Lesson
from ..models.LessonTypeChoices import LessonTypeChoices


@shared_task(base=Singleton)
def update_user_lesson_parent_task(lesson_id: int, user_id: int):
    from ..models.UserLesson import UserLesson

    with transaction.atomic(using='master'):
        lesson = Lesson.objects.get(pk=lesson_id)
        parent = lesson.parent

        if lesson.lesson_type == LessonTypeChoices.THEME.value or not parent:
            return 'Nothing can be done with this "lesson_id".'

        lesson_ids = Lesson.objects.filter(**{
            'parent_id': parent.id,
        }).values_list('id', flat=True)

        completed_lessons = UserLesson.objects.using('master').filter(**{
            'lesson_id__in': lesson_ids,
            'completed_at__isnull': False,
        }).values_list('id', flat=True)

        if len(lesson_ids) == len(completed_lessons):
            parent, is_created = UserLesson.objects.using(
                'master'
            ).get_or_create(**{
                'lesson': parent,
                'user_id': user_id,
            })

            parent.completed_at = timezone.now()
            parent.save()

            return 'Parent Lesson is updated.'

        return 'Parent Lesson is not updated.'
