from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils import timezone

from courses.models.Course import Course
from courses.models.CourseStat import CourseStat
from events.models.Event import Event
from events.models.New import New

from .CommentedTypeChoices import CommentedTypeChoices as CTChoices


class Comment(models.Model):
    author = models.ForeignKey(**{
        'to': 'users.User',
        'on_delete': models.CASCADE,
        'help_text': 'The user who wrote the comment.',
    })
    body = models.TextField(**{
        'help_text': 'The text of the comment itself.',
    })
    created_at = models.DateTimeField(**{
        'default': timezone.now,
        'help_text': 'Date the comment was written.',
    })
    commented_type = models.SmallIntegerField(choices=CTChoices.choices)
    commented_id = models.PositiveBigIntegerField(**{
        'help_text': 'ID of the object for which the comment is written.',
    })
    rating = models.PositiveSmallIntegerField(**{
        'default': None,
        'null': True,
        'blank': True,
        'help_text': 'The rating set by the user along with the comment.',
    })

    class Meta:
        indexes = [
            models.Index(fields=['commented_type', 'commented_id'])
        ]

    def __str__(self):
        return (
            f'{self.created_at} | {self.commented_type}: {self.commented_id} -'
            f' {self.author}'
        )

    def __iter__(self):
        for key in self.__dict__:
            if not key.startswith('_'):
                yield key, getattr(self, key)

    def save(self, *args, **kwargs):
        self.full_clean()

        try:
            self._check_commented_id_as_foreign_key()
        except ObjectDoesNotExist:
            detail = {
                'commented_id': 'Object with this id is not found'
            }
            raise ValidationError(detail)

        if self.pk is None and self.commented_type == CTChoices.COURSE.value:
            self._update_course_stat('add')

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.commented_type == CTChoices.COURSE.value:
            self._update_course_stat('sub')

        super().delete(*args, **kwargs)

    def _check_commented_id_as_foreign_key(self):
        if self.commented_type == CTChoices.COURSE.value:
            Course.objects.get(pk=self.commented_id)

        if self.commented_type == CTChoices.NEWS.value:
            New.objects.get(pk=self.commented_id)

        if self.commented_type == CTChoices.EVENT.value:
            Event.objects.get(pk=self.commented_id)

    def _update_course_stat(self, type_operation):
        if type_operation == 'add':
            change_count_rating = 1
        elif type_operation == 'sub':
            change_count_rating = -1
        else:
            raise Exception('Not valid arg "type_operation".')

        course_stat = CourseStat.objects.get(course_id=self.commented_id)

        rating = self.rating
        if rating == 5:
            course_stat.count_five_rating += change_count_rating
        elif rating == 4:
            course_stat.count_four_rating += change_count_rating
        elif rating == 3:
            course_stat.count_three_rating += change_count_rating
        elif rating == 2:
            course_stat.count_two_rating += change_count_rating
        else:
            course_stat.count_one_rating += change_count_rating

        course_stat.save()
