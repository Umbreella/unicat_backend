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

    def save(self, *args, **kwargs):
        self.count_comments = self.count_five_rating + \
                              self.count_four_rating + \
                              self.count_three_rating + \
                              self.count_two_rating + \
                              self.count_one_rating

        if self.count_comments != 0:
            self.avg_rating = (self.count_five_rating * 5 +
                               self.count_four_rating * 4 +
                               self.count_three_rating * 3 +
                               self.count_two_rating * 2 +
                               self.count_one_rating) / self.count_comments
        else:
            self.avg_rating = 0

        super().save(*args, **kwargs)
