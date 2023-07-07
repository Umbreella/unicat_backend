import uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone


def add_ten_minutes():
    return timezone.now() + timedelta(minutes=10)


class ResetPassword(models.Model):
    user = models.ForeignKey(**{
        'to': 'users.User',
        'on_delete': models.CASCADE,
        'help_text': 'The user who requested a password change.',
    })
    url = models.UUIDField(**{
        'primary_key': True,
        'default': uuid.uuid4,
        'editable': False,
        'help_text': 'A unique link to change your password.',
    })
    closed_at = models.DateTimeField(**{
        'default': add_ten_minutes,
        'help_text': 'Duration of the change request.',
    })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
