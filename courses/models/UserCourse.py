from django.db import models
from django.utils import timezone

from .Course import Course


class UserCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='user_courses')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,
                             related_name='my_progress')
    count_lectures_completed = models.PositiveSmallIntegerField(default=0)
    count_independents_completed = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    last_view = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(default=None, null=True, blank=True)

    class Meta:
        unique_together = [['course', 'user']]

    def __iter__(self):
        for key in self.__dict__:
            if not key.startswith('_'):
                yield key, getattr(self, key)

    def save(self, *args, **kwargs):
        self.full_clean()

        course_count_data = [
            self.course.count_lectures,
            self.course.count_independents,
        ]

        user_course_count_data = [
            self.count_lectures_completed,
            self.count_independents_completed,
        ]

        if course_count_data == user_course_count_data:
            self.completed_at = timezone.now()

        super().save(*args, **kwargs)
