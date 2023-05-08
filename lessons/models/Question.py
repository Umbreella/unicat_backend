from django.db import models

from ..tasks.UpdateCountQuestionTask import update_count_question_task
from .Lesson import Lesson
from .QuestionTypeChoices import QuestionTypeChoices as QTChoices


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                               related_name='questions')
    body = models.CharField(max_length=512)
    question_type = models.PositiveSmallIntegerField(choices=QTChoices.choices)

    def __iter__(self):
        for key in self.__dict__:
            if not key.startswith('_'):
                yield key, getattr(self, key)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        update_count_question_task.apply_async(kwargs={
            'lesson_id': self.lesson_id,
        })

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        update_count_question_task.apply_async(kwargs={
            'lesson_id': self.lesson_id,
        })
