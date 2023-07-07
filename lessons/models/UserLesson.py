from django.db import models

from ..models.Lesson import Lesson
from ..tasks.UpdateUserCourseCountTask import update_user_course_count_task
from ..tasks.UpdateUserLessonParentTask import update_user_lesson_parent_task


class UserLesson(models.Model):
    lesson = models.ForeignKey(**{
        'to': Lesson,
        'on_delete': models.CASCADE,
        'related_name': 'progress',
        'help_text': 'A lesson that the user has access to.',
    })
    user = models.ForeignKey(**{
        'to': 'users.User',
        'on_delete': models.CASCADE,
        'help_text': 'The user who got access to the lesson.',
    })
    completed_at = models.DateField(**{
        'default': None,
        'null': True,
        'blank': True,
        'help_text': 'Has the lesson been completed by the user.',
    })

    class Meta:
        unique_together = [
            ['lesson', 'user', ],
        ]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        if self.completed_at:
            update_user_lesson_parent_task.apply_async(kwargs={
                'lesson_id': self.lesson_id,
                'user_id': self.user_id,
            })

            update_user_course_count_task.apply_async(kwargs={
                'lesson_id': self.lesson_id,
                'user_id': self.user_id,
            })
