from django.db import models

from .Course import Course


class CourseStat(models.Model):
    course = models.OneToOneField(**{
        'to': Course,
        'on_delete': models.CASCADE,
        'related_name': 'statistic',
        'help_text': 'The course for which statistics are collected.',
    })
    count_comments = models.PositiveIntegerField(**{
        'default': 0,
        'help_text': 'Total number of all comments.',
    })
    count_five_rating = models.PositiveIntegerField(**{
        'default': 0,
        'help_text': (
            'Number of comments with a rating of 5, calculated at the time '
            'of creating a comment to the course'
        ),
    })
    count_four_rating = models.PositiveIntegerField(**{
        'default': 0,
        'help_text': (
            'Number of comments with a rating of 4, calculated at the time '
            'of creating a comment to the course'
        ),
    })
    count_three_rating = models.PositiveIntegerField(**{
        'default': 0,
        'help_text': (
            'Number of comments with a rating of 3, calculated at the time '
            'of creating a comment to the course'
        ),
    })
    count_two_rating = models.PositiveIntegerField(**{
        'default': 0,
        'help_text': (
            'Number of comments with a rating of 2, calculated at the time '
            'of creating a comment to the course'
        ),
    })
    count_one_rating = models.PositiveIntegerField(**{
        'default': 0,
        'help_text': (
            'Number of comments with a rating of 1, calculated at the time '
            'of creating a comment to the course'
        ),
    })

    def __iter__(self):
        for key in self.__dict__:
            if not key.startswith('_'):
                yield key, getattr(self, key)

    def save(self, *args, **kwargs):
        self.full_clean()

        self.count_comments = sum([
            self.count_five_rating,
            self.count_four_rating,
            self.count_three_rating,
            self.count_two_rating,
            self.count_one_rating,
        ])

        if self.count_comments != 0:
            sum_rating = sum([
                self.count_five_rating * 5,
                self.count_four_rating * 4,
                self.count_three_rating * 3,
                self.count_two_rating * 2,
                self.count_one_rating,
            ])

            self.course.avg_rating = round(sum_rating / self.count_comments, 2)
        else:
            self.course.avg_rating = 0

        super().save(*args, **kwargs)
        self.course.save()
