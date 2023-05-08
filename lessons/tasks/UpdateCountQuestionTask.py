from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction

from ..models.Lesson import Lesson


@shared_task(base=Singleton)
def update_count_question_task(lesson_id: int):
    from ..models.Question import Question

    with transaction.atomic(using='master'):
        lesson = Lesson.objects.using('master').get(pk=lesson_id)

        count_question = Question.objects.filter(**{
            'lesson': lesson,
        }).using('master').count()

        lesson.count_questions = count_question
        lesson.save()

        return 'Count question is updated/'
