from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction

from courses.models.Course import Course

from ..models.LessonTypeChoices import LessonTypeChoices


@shared_task(base=Singleton)
def update_count_lesson_task(course_id: int, lesson_type: int):
    from ..models.Lesson import Lesson

    if lesson_type not in LessonTypeChoices.values:
        detail = '"lesson_type" is not valid.'
        raise Exception(detail)

    if lesson_type == LessonTypeChoices.THEME.value:
        return 'Count lesson is not updated.'

    with transaction.atomic(using='master'):
        course = Course.objects.using('master').get(pk=course_id)

        if lesson_type == LessonTypeChoices.THEORY.value:
            count_lectures = Lesson.objects.filter(**{
                'course': course,
                'lesson_type': lesson_type,
            }).using('master').count()

            course.count_lectures = count_lectures
            course.save()

        if lesson_type == LessonTypeChoices.TEST.value:
            count_independents = Lesson.objects.filter(**{
                'course': course,
                'lesson_type': lesson_type,
            }).using('master').count()

            course.count_independents = count_independents
            course.save()

        return 'Count lesson is updated.'
