from django.db import models


class Event(models.Model):
    preview = models.ImageField(upload_to='events/%Y/%m/%d/')
    title = models.CharField(max_length=255, default='')
    short_description = models.CharField(max_length=255, default='')
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    place = models.CharField(max_length=255, default='')

    class Meta:
        abstract = False

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)
