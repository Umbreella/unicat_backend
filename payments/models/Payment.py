from django.db import models
from django.utils import timezone

from courses.models.Course import Course
from users.models import User

from ..tasks.CreateUserCourseTask import create_user_course_task


class Payment(models.Model):
    id = models.CharField(max_length=27, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='payments')
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    is_success = models.BooleanField(default=False)

    def __iter__(self):
        for key in self.__dict__:
            if not key.startswith('_'):
                yield key, getattr(self, key)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        if self.id and self.is_success:
            create_user_course_task.apply_async(kwargs={
                'course_id': self.course_id,
                'user_id': self.user_id,
            })
