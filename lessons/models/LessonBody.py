from django.db import models

from .Lesson import Lesson


class LessonBody(models.Model):
    lesson = models.OneToOneField(**{
        'to': Lesson,
        'on_delete': models.CASCADE,
        'related_name': 'lesson_body',
        'help_text': 'The lesson to which the full content refers.',
    })
    body = models.TextField(**{
        'help_text': 'Full content of the lesson.',
    })

    def __iter__(self):
        for key in self.__dict__:
            if not key.startswith('_'):
                yield key, getattr(self, key)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
