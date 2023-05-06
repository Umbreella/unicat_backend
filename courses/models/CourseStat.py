from django.db import models

from .Course import Course


class CourseStat(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE,
                                  related_name='statistic')
    avg_rating = models.DecimalField(default=0, max_digits=2, decimal_places=1)
    count_comments = models.PositiveIntegerField(default=0)
    count_five_rating = models.PositiveIntegerField(default=0)
    count_four_rating = models.PositiveIntegerField(default=0)
    count_three_rating = models.PositiveIntegerField(default=0)
    count_two_rating = models.PositiveIntegerField(default=0)
    count_one_rating = models.PositiveIntegerField(default=0)

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

            self.avg_rating = sum_rating / self.count_comments
        else:
            self.avg_rating = 0

        super().save(*args, **kwargs)
