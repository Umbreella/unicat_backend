from django.db import models

from ..tasks.UpdateCountLessonTask import update_count_lesson_task
from .LessonTypeChoices import LessonTypeChoices as LTChoices


class Lesson(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE,
                               related_name='lessons')
    serial_number = models.PositiveSmallIntegerField(default=1)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               null=True, default=None, blank=True,
                               related_name='children')
    title = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='')
    lesson_type = models.PositiveSmallIntegerField(choices=LTChoices.choices)
    time_limit = models.DurationField(null=True, default=None, blank=True)
    count_questions = models.PositiveSmallIntegerField(default=0)

    listeners = models.ManyToManyField('users.User', through='UserLesson',
                                       related_name='my_lessons')

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
