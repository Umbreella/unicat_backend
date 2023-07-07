from django.db import models
from django.utils import timezone


class Feedback(models.Model):
    name = models.CharField(**{
        'max_length': 255,
        'help_text': 'Full name of the user who wrote.',
    })
    email = models.EmailField(**{
        'max_length': 128,
        'help_text': 'Email of the user who wrote.',
    })
    body = models.TextField(**{
        'help_text': 'Message content.',
    })
    created_at = models.DateTimeField(**{
        'default': timezone.now,
        'help_text': 'Date of writing the message.',
    })
    is_closed = models.BooleanField(**{
        'default': False,
        'help_text': 'Has the message been processed.',
    })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
