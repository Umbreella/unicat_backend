from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone

from ..models.Course import Course


class Discount(models.Model):
    course = models.ForeignKey(**{
        'to': Course,
        'on_delete': models.CASCADE,
        'related_name': 'discounts',
        'help_text': 'The course for which the discount was created.',
    })
    percent = models.IntegerField(**{
        'validators': [MinValueValidator(1), MaxValueValidator(100), ],
        'help_text': 'Discount percentage, from 0 to 100.',
    })
    start_date = models.DateTimeField(**{
        'help_text': 'Discount start date.',
    })
    end_date = models.DateTimeField(**{
        'help_text': 'Discount end date.',
    })

    def __str__(self):
        return f'{self.course} - {self.percent}%'

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.pk and self.start_date.date() <= timezone.now().date():
            detail = {
                'start_date': [
                    'Discount must start no earlier than tomorrow.',
                ],
            }
            raise ValidationError(detail)

        if self.start_date >= self.end_date:
            detail = {
                'start_date': [
                    'Erroneous date values.',
                ],
                'end_date': [
                    'Erroneous date values.',
                ],
            }
            raise ValidationError(detail)

        if Discount.objects.filter(
                Q(course=self.course) & (
                        Q(end_date__range=(self.start_date, self.end_date,)) |
                        Q(start_date__range=(self.start_date, self.end_date,))
                )
        ).exclude(pk=self.pk).exists():
            detail = {
                '__all__': [
                    'This course has other discounts for this interval.',
                ],
            }
            raise ValidationError(detail)

        super().save(*args, **kwargs)
