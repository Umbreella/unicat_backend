from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction

from courses.models.UserCourse import UserCourse

from ..models.Lesson import Lesson
from ..models.LessonTypeChoices import LessonTypeChoices


@shared_task(base=Singleton)
def update_user_course_task(lesson_id: int, user_id: int):
    from ..models.UserLesson import UserLesson

    with transaction.atomic(using='master'):
        lesson = Lesson.objects.select_related(
            'course'
        ).using('master').get(pk=lesson_id)
        lesson_type = lesson.lesson_type
        course = lesson.course

        if lesson_type == LessonTypeChoices.THEME.value:
            return 'User Course is not updated.'

        user_course = UserCourse.objects.using('master').get(**{
            'course': course,
            'user_id': user_id,
        })

        count_completed_lesson = UserLesson.objects.filter(**{
            'lesson__course': course,
            'user_id': user_id,
            'lesson__lesson_type': lesson_type,
            'completed_at__isnull': False,
        }).using('master').count()

        if lesson_type == LessonTypeChoices.THEORY.value:
            user_course.count_lectures_completed = count_completed_lesson
        elif lesson_type == LessonTypeChoices.TEST.value:
            user_course.count_independents_completed = count_completed_lesson

        user_course.save()

        return 'User Course is updated.'
