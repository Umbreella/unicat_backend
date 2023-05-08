from django.core.cache import cache
from django.db import models
from graphene import relay

from unicat.graphql.functions import get_timeout_seconds

from ..schema.UserAttemptType import UserAttemptType
from .Question import Question
from .UserAttempt import UserAttempt


class UserAnswer(models.Model):
    user_attempt = models.ForeignKey(UserAttempt, on_delete=models.CASCADE,
                                     related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='user_answers')
    is_true = models.BooleanField(default=False)

    class Meta:
        unique_together = [
            ['user_attempt', 'question', ],
        ]

    def __iter__(self):
        for key in self.__dict__:
            if not key.startswith('_'):
                yield key, getattr(self, key)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        if self.is_true:
            self.user_attempt.count_true_answer += 1
            self.user_attempt.save()

        self.__cache_answered_question_id()

    def __cache_answered_question_id(self):
        user_attempt = self.user_attempt
        attempt_id = user_attempt.id
        time_end = user_attempt.time_end

        global_attempt_id = relay.Node.to_global_id(**{
            'type_': UserAttemptType,
            'id': attempt_id,
        })

        answered_questions_id = UserAnswer.objects.filter(**{
            'user_attempt_id': attempt_id,
        }).values('question_id').using('master')

        cache_key = f'{global_attempt_id}_answered_questions'
        cache_value = [
            item['question_id'] for item in answered_questions_id
        ]
        cache_timeout = get_timeout_seconds(time_end)

        cache.set(cache_key, cache_value, cache_timeout)
