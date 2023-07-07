from django.core.cache import cache
from django.db import models
from django.utils import timezone
from graphene import relay

from .UserLesson import UserLesson


class UserAttempt(models.Model):
    user_lesson = models.ForeignKey(**{
        'to': UserLesson,
        'on_delete': models.CASCADE,
        'help_text': 'The user lesson to which the attempt is attached.',
    })
    time_start = models.DateTimeField(**{
        'default': timezone.now,
        'help_text': 'Attempt start time.',
    })
    time_end = models.DateTimeField(**{
        'default': None,
        'null': True,
        'blank': True,
        'help_text': 'Attempt completion time.',
    })
    count_true_answer = models.PositiveSmallIntegerField(**{
        'default': 0,
        'help_text': 'The number of correct answers.',
    })

    def save(self, *args, **kwargs):
        self.full_clean()

        time_limit = self.user_lesson.lesson.time_limit

        if self.time_end is None and time_limit:
            self.time_end = self.time_start + time_limit

        if self.id:
            self.__update_time_end()

        super().save(*args, **kwargs)

    def __update_time_end(self):
        from ..schema.UserAttemptType import UserAttemptType

        global_attempt_id = relay.Node.to_global_id(**{
            'type_': UserAttemptType,
            'id': self.id,
        })
        cache_key = f'{global_attempt_id}_answered_questions'
        answered_question_ids = cache.get(cache_key, [])
        count_answer = len(answered_question_ids)

        count_questions = self.user_lesson.lesson.count_questions

        if count_answer == count_questions:
            self.time_end = timezone.now()
            cache.delete(cache_key)

        if self.user_lesson.completed_at:
            return None

        if count_questions > 0 and (
                (self.count_true_answer / count_questions) >= 0.6
        ):
            self.user_lesson.completed_at = timezone.now()
            self.user_lesson.save()
