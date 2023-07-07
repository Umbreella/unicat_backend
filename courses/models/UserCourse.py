from django.db import models
from django.utils import timezone

from ..tasks.UpdateCourseCountListenersTask import \
    update_course_count_listeners_task
from .Course import Course


class UserCourse(models.Model):
    course = models.ForeignKey(**{
        'to': Course,
        'on_delete': models.CASCADE,
        'related_name': 'user_courses',
        'help_text': 'The course that has been accessed.'
    })
    user = models.ForeignKey(**{
        'to': 'users.User',
        'on_delete': models.CASCADE,
        'related_name': 'my_progress',
        'help_text': 'The user who gained access.'
    })
    count_lectures_completed = models.PositiveSmallIntegerField(**{
        'default': 0,
        'help_text': (
            'The number of lectures delivered by the user from the course, '
            'calculated automatically.'
        ),
    })
    count_independents_completed = models.PositiveSmallIntegerField(**{
        'default': 0,
        'help_text': (
            'The number of independent tasks performed by the user from the '
            'course, calculated automatically.'
        ),
    })
    created_at = models.DateTimeField(**{
        'default': timezone.now,
        'help_text': 'Access creation time.',
    })
    last_view = models.DateTimeField(**{
        'default': timezone.now,
        'help_text': (
            'The date of the last viewing of the lesson from the course.'
        ),
    })
    completed_at = models.DateTimeField(**{
        'default': None,
        'null': True,
        'blank': True,
        'help_text': (
            'Have you completed enough lessons to consider the course '
            'completed at a minimum'
        ),
    })

    class Meta:
        unique_together = [
            ['course', 'user', ],
        ]

    def __iter__(self):
        for key in self.__dict__:
            if not key.startswith('_'):
                yield key, getattr(self, key)

    def save(self, *args, **kwargs):
        from ..loaders.UserProgressLoader import get_progress

        self.full_clean()

        if get_progress(self) >= 60:
            self.completed_at = timezone.now()

        is_create = self.id is None

        super().save(*args, **kwargs)

        if is_create:
            update_course_count_listeners_task.apply_async(kwargs={
                'course_id': self.course_id,
            })
