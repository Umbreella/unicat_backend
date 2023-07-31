from django.db import models
from django.utils import timezone

from courses.models.Course import Course
from users.models import User

from ..tasks.CreateUserCourseTask import create_user_course_task


class Payment(models.Model):
    id = models.CharField(**{
        'max_length': 27,
        'primary_key': True,
        'help_text': 'Payment intent ID from StripeAPI.',
    })
    user = models.ForeignKey(**{
        'to': User,
        'on_delete': models.CASCADE,
        'related_name': 'payments',
        'help_text': 'The user for whom the payment was created.',
    })
    course = models.ForeignKey(**{
        'to': Course,
        'on_delete': models.CASCADE,
        'related_name': 'payments',
        'help_text': 'The course for which the payment was created.',
    })
    amount = models.DecimalField(**{
        'max_digits': 9,
        'decimal_places': 2,
        'help_text': 'Amount of payment.',
    })
    created_at = models.DateTimeField(**{
        'default': timezone.now,
        'help_text': 'Payment creation time.',
    })
    is_success = models.BooleanField(**{
        'default': False,
        'help_text': 'Payment status.',
    })

    def __iter__(self):
        for key in self.__dict__:
            if not key.startswith('_'):
                yield key, getattr(self, key)

    def save(self, *args, **kwargs):
        if isinstance(self.amount, float):
            self.amount = str(round(self.amount, 2))

        self.full_clean()
        super().save(*args, **kwargs)

        if self.id and self.is_success:
            create_user_course_task.apply_async(kwargs={
                'course_id': self.course_id,
                'user_id': self.user_id,
            })
