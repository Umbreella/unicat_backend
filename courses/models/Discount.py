from django.db import models

from ..models.Course import Course


class Discount(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE,
                               related_name='discounts')
    new_price = models.DecimalField(max_digits=7, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        abstract = False

    def __str__(self):
        return f'{self.course} - {self.new_price} (before {self.end_date})'

    def save(self, *args, **kwargs):
        course_base_price = self.course.price
        course_new_price = self.new_price
        start_date_discount = self.start_date
        end_date_discount = self.end_date

        update_fields = []
        if course_new_price <= course_base_price:
            update_fields += ['new_price']

        if start_date_discount <= end_date_discount:
            update_fields += ['start_date', 'end_date']

        if self.pk:
            kwargs.update({
                'update_fields': update_fields
            })
        elif len(update_fields) != 3:
            return None

        super().save(*args, **kwargs)
