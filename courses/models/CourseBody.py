from django.db import models

from .Course import Course


class CourseBody(models.Model):
    course = models.OneToOneField(**{
        'to': Course,
        'on_delete': models.CASCADE,
        'related_name': 'course_body',
        'help_text': 'The course for which you need to create its content.',
    })
    body = models.TextField(**{
        'help_text': 'Course content displayed on the Description tab.',
    })

    def __str__(self):
        return f'{self.course} - {self.body[:50]}'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
