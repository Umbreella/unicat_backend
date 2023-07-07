from django.db import models

from .Question import Question


class AnswerValue(models.Model):
    question = models.ForeignKey(**{
        'to': Question,
        'on_delete': models.CASCADE,
        'related_name': 'answers',
        'help_text': 'The question to which this answer was created.',
    })
    value = models.CharField(**{
        'max_length': 128,
        'help_text': 'Answer body.',
    })
    is_true = models.BooleanField(**{
        'default': False,
        'help_text': 'Is this answer correct or not.',
    })

    def save(self, *args, **kwargs):
        self.value = self.value.strip()

        self.full_clean()

        super().save(*args, **kwargs)
