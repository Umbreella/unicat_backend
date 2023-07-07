from django.db import models
from django.utils import timezone

from ..tasks.UpdateTeacherInfoTask import update_teacher_info_task
from .Category import Category
from .LearningFormat import LearningFormat


class Course(models.Model):
    teacher = models.ForeignKey(**{
        'to': 'users.Teacher',
        'on_delete': models.SET_NULL,
        'null': True,
        'help_text': 'The teacher who leads the course.',
    })
    category = models.ForeignKey(**{
        'to': Category,
        'on_delete': models.SET_NULL,
        'null': True,
        'related_name': 'courses',
        'help_text': 'Course category.',
    })
    listeners = models.ManyToManyField(**{
        'to': 'users.User',
        'through': 'UserCourse',
        'related_name': 'my_courses',
        'help_text': 'All students of the course.',
    })
    title = models.CharField(**{
        'max_length': 128,
        'default': '',
        'help_text': 'Course name.',
    })
    price = models.DecimalField(**{
        'max_digits': 7,
        'decimal_places': 2,
        'help_text': 'Course price.',
    })
    count_lectures = models.PositiveSmallIntegerField(**{
        'default': 0,
        'help_text': 'Count lectures in course, calculated automatically.',
    })
    count_independents = models.PositiveSmallIntegerField(**{
        'default': 0,
        'help_text': 'Count independents in course, calculated automatically.',
    })
    count_listeners = models.PositiveSmallIntegerField(**{
        'default': 0,
        'help_text': 'Count listeners in course, calculated automatically.',
    })
    duration = models.PositiveIntegerField(default=1)
    learning_format = models.IntegerField(choices=LearningFormat.choices)
    preview = models.ImageField(**{
        'upload_to': 'courses/%Y/%m/%d/',
        'help_text': 'Course picture.',
    })
    short_description = models.CharField(**{
        'max_length': 255,
        'default': '',
        'help_text': 'A few words about the course, shown on the course icon.',
    })
    avg_rating = models.DecimalField(**{
        'default': 0,
        'max_digits': 2,
        'decimal_places': 1,
        'help_text': (
            'Average rating based on comments, calculated automatically.'
        ),
    })
    created_at = models.DateTimeField(**{
        'default': timezone.now,
        'help_text': 'Course creation time.',
    })

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if isinstance(self.price, float):
            self.price = str(self.price)

        if isinstance(self.avg_rating, float):
            self.avg_rating = str(self.avg_rating)

        self.full_clean()
        super().save(*args, **kwargs)

        if not hasattr(self, 'statistic'):
            from .CourseStat import CourseStat

            CourseStat.objects.create(**{
                'course': self,
            })

        update_teacher_info_task.apply_async(kwargs={
            'teacher_id': self.teacher_id,
        })
