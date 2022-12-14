from django.db import models

from ..models.Course import Course


class ShortLesson(models.Model):
    serial_number = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='')
    parent_lesson = models.ForeignKey('self',
                                      on_delete=models.SET_NULL, null=True,
                                      default=None, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True,
                               default=None, blank=True)

    class Meta:
        abstract = False

    def __str__(self):
        parent_serial_number = ""

        if self.parent_lesson:
            parent_serial_number = str(self.parent_lesson).split(' ')[0]

        return f'{parent_serial_number}{self.serial_number}. {self.title}'

    def __iter__(self):
        for key in self.__dict__:
            if key != '_state':
                yield key, getattr(self, key)

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)
