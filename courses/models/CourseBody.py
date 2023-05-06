from django.db import models

from .Course import Course


class CourseBody(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE,
                                  related_name='course_body')
    body = models.TextField()

    def __str__(self):
        return f'{self.course} - {self.body[:50]}'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
