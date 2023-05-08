from django.db import models

from .Lesson import Lesson


class LessonBody(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE,
                                  related_name='lesson_body')
    body = models.TextField()

    def __iter__(self):
        for key in self.__dict__:
            if not key.startswith('_'):
                yield key, getattr(self, key)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
