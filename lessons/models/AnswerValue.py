from django.db import models

from .Question import Question


class AnswerValue(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='answers')
    value = models.CharField(max_length=128)
    is_true = models.BooleanField(default=True)

    def __iter__(self):
        for key in self.__dict__:
            if not key.startswith('_'):
                yield key, getattr(self, key)

    def save(self, *args, **kwargs):
        self.full_clean()

        self.value = self.value.strip()

        super().save(*args, **kwargs)
