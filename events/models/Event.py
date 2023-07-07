from django.db import models
from django.utils import timezone


class Event(models.Model):
    preview = models.ImageField(**{
        'upload_to': 'events/%Y/%m/%d/',
        'help_text': 'Event image.',
    })
    title = models.CharField(**{
        'max_length': 255,
        'default': '',
        'help_text': 'Event name.',
    })
    short_description = models.CharField(**{
        'max_length': 255,
        'default': '',
        'help_text': 'A brief description of the event displayed on the icon.',
    })
    description = models.TextField(**{
        'help_text': 'Full description of the event.',
    })
    date = models.DateField(**{
        'help_text': 'Event date.',
    })
    start_time = models.TimeField(**{
        'help_text': 'Event start time.',
    })
    end_time = models.TimeField(**{
        'help_text': 'Event end time.',
    })
    place = models.CharField(**{
        'max_length': 255,
        'default': '',
        'help_text': 'Venue of the event.',
    })
    created_at = models.DateTimeField(**{
        'default': timezone.now,
        'help_text': 'Event creation time.',
    })

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
