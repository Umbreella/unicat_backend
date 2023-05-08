from django.core.cache import cache
from django.db import models
from django.utils import timezone
from graphene import relay

from .UserLesson import UserLesson


class UserAttempt(models.Model):
    user_lesson = models.ForeignKey(UserLesson, on_delete=models.CASCADE)
    time_start = models.DateTimeField(default=timezone.now)
    time_end = models.DateTimeField(default=None, null=True, blank=True)
    count_true_answer = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.full_clean()

        time_limit = self.user_lesson.lesson.time_limit

        if self.time_end is None and time_limit:
            self.time_end = self.time_start + time_limit

        if self.id:
            self.__update_time_end()

        super().save(*args, **kwargs)
        self.__update_user_lesson()

    def __update_time_end(self):
        from ..schema.UserAttemptType import UserAttemptType

        global_attempt_id = relay.Node.to_global_id(**{
            'type_': UserAttemptType,
            'id': self.id,
        })
        cache_key = f'{global_attempt_id}_answered_questions'
        answered_question_ids = cache.get(cache_key, [])
        count_answer = len(answered_question_ids)

        if count_answer == self.user_lesson.lesson.count_questions:
            self.time_end = timezone.now()
            cache.delete(cache_key)

    def __update_user_lesson(self):
        user_lesson = self.user_lesson

        if user_lesson.completed_at:
            return None

        lesson = user_lesson.lesson
        lesson_count_questions = lesson.count_questions
        count_true_answer = self.count_true_answer

        if lesson_count_questions == 0:
            return None

        percent_quality = (
            round(count_true_answer / lesson_count_questions * 100)
        )

        if percent_quality >= 60:
            user_lesson.completed_at = timezone.now()
            user_lesson.save()
