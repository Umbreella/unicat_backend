from django.db import models

from ..models.Lesson import Lesson
from ..tasks.UpdateUserCourseTask import update_user_course_task
from ..tasks.UpdateUserLessonParentTask import update_user_lesson_parent_task


class UserLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                               related_name='progress')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    completed_at = models.DateField(default=None, null=True, blank=True)

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

            update_user_course_task.apply_async(kwargs={
                'lesson_id': self.lesson_id,
                'user_id': self.user_id,
            })
