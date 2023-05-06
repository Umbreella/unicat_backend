from django.db import models
from django.utils import timezone

from .Category import Category
from .LearningFormat import LearningFormat


class Course(models.Model):
    teacher = models.ForeignKey('users.Teacher', on_delete=models.SET_NULL,
                                null=True)
    title = models.CharField(max_length=128, default='')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount = models.DecimalField(max_digits=7, decimal_places=2,
                                   default=None, null=True, blank=True)
    count_lectures = models.PositiveSmallIntegerField(default=0)
    count_independents = models.PositiveSmallIntegerField(default=0)
    duration = models.PositiveIntegerField(default=1)
    learning_format = models.IntegerField(choices=LearningFormat.choices)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL,
                                 null=True, related_name='courses')
    preview = models.ImageField(upload_to='courses/%Y/%m/%d/')
    short_description = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(default=timezone.now)

    listeners = models.ManyToManyField('users.User', through='UserCourse',
                                       related_name='my_courses')

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        if not hasattr(self, 'statistic'):
            from .CourseStat import CourseStat

            CourseStat.objects.create(**{
                'course': self,
            })
