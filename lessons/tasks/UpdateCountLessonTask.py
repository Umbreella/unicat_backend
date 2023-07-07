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
        update_data = {}

        if lesson_type == LessonTypeChoices.THEORY.value:
            count_lectures = Lesson.objects.filter(**{
                'course_id': course_id,
                'lesson_type': lesson_type,
            }).count()

            update_data.update({
                'count_lectures': count_lectures,
            })

        if lesson_type == LessonTypeChoices.TEST.value:
            count_independents = Lesson.objects.filter(**{
                'course_id': course_id,
                'lesson_type': lesson_type,
            }).count()

            update_data.update({
                'count_independents': count_independents,
            })

        Course.objects.filter(**{
            'pk': course_id,
        }).update(**update_data)

        return 'Count lesson is updated.'
