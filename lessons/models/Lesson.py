from django.db import models

from ..tasks.UpdateCountLessonTask import update_count_lesson_task
from .LessonTypeChoices import LessonTypeChoices as LTChoices


class Lesson(models.Model):
    course = models.ForeignKey(**{
        'to': 'courses.Course',
        'on_delete': models.CASCADE,
        'related_name': 'lessons',
        'help_text': 'The course that the lesson belongs to.',
    })
    parent = models.ForeignKey(**{
        'to': 'self',
        'on_delete': models.SET_NULL,
        'null': True,
        'default': None,
        'blank': True,
        'related_name': 'children',
        'help_text': 'Parent lesson in relation to the current.',
    })
    serial_number = models.PositiveSmallIntegerField(**{
        'default': 1,
        'help_text': 'Sequence number of the lesson.',
    })
    title = models.CharField(**{
        'max_length': 255,
        'default': '',
        'help_text': 'Lesson name.',
    })
    description = models.CharField(**{
        'max_length': 255,
        'default': '',
        'help_text': (
            'A brief description of the lesson, which is displayed in the '
            'course content tab.'
        ),
    })
    lesson_type = models.PositiveSmallIntegerField(**{
        'choices': LTChoices.choices,
        'help_text': 'Type of lesson.',
    })
    time_limit = models.DurationField(**{
        'null': True,
        'default': None,
        'blank': True,
        'help_text': 'time limit for tests, if necessary.',
    })
    count_questions = models.PositiveSmallIntegerField(**{
        'default': 0,
        'help_text': (
            'The number of questions in the test, calculated automatically.'
        ),
    })
    listeners = models.ManyToManyField(**{
        'to': 'users.User',
        'through': 'UserLesson',
        'related_name': 'my_lessons',
        'help_text': 'All users who have access to the lesson.',
    })

    def __iter__(self):
        for key in self.__dict__:
            if not key.startswith('_'):
                yield key, getattr(self, key)

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.parent is not None:
            self.course = self.parent.course

        super().save(*args, **kwargs)

        update_count_lesson_task.apply_async(kwargs={
            'course_id': self.course_id,
            'lesson_type': self.lesson_type,
        })
