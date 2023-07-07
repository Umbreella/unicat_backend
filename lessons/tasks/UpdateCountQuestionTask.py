from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction

from ..models.Lesson import Lesson


@shared_task(base=Singleton)
def update_count_question_task(lesson_id: int):
    from ..models.Question import Question

    with transaction.atomic(using='master'):
        count_question = Question.objects.using('master').filter(**{
            'lesson_id': lesson_id,
        }).count()

        Lesson.objects.filter(**{
            'pk': lesson_id,
        }).update(**{
            'count_questions': count_question,
        })

        return 'Count question is updated/'
