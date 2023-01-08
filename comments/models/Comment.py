from django.db import models
from django.utils import timezone

from courses.models.CourseStat import CourseStat

from .CommentedType import CommentedType


class Comment(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    count_like = models.PositiveSmallIntegerField(default=0)
    commented_type = models.CharField(max_length=8,
                                      choices=CommentedType.choices)
    commented_id = models.PositiveBigIntegerField()
    rating = models.PositiveSmallIntegerField(default=None, null=True,
                                              blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['commented_type', 'commented_id'])
        ]

    def __str__(self):
        return f'{self.created_at} | {self.commented_type}:' \
               f'{self.commented_id} - {self.author}'

    def __iter__(self):
        for key in self.__dict__:
            if key != '_state':
                yield key, getattr(self, key)

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.pk and self.commented_type == CommentedType.COURSE.value:
            course_stat = CourseStat.objects.get(course_id=self.commented_id)

            rating = self.rating
            if rating == 5:
                course_stat.count_five_rating += 1
            elif rating == 4:
                course_stat.count_four_rating += 1
            elif rating == 3:
                course_stat.count_three_rating += 1
            elif rating == 2:
                course_stat.count_two_rating += 1
            else:
                course_stat.count_one_rating += 1

            course_stat.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.commented_type == CommentedType.COURSE.value:
            course_stat = CourseStat.objects.get(course_id=self.commented_id)

            rating = self.rating
            if rating == 5:
                course_stat.count_five_rating -= 1
            elif rating == 4:
                course_stat.count_four_rating -= 1
            elif rating == 3:
                course_stat.count_three_rating -= 1
            elif rating == 2:
                course_stat.count_two_rating -= 1
            else:
                course_stat.count_one_rating -= 1

            course_stat.save()

        super().delete(*args, **kwargs)
