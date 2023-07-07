import uuid
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .User import User


def add_ten_minutes():
    return timezone.now() + timedelta(minutes=10)


class ChangeEmail(models.Model):
    user = models.ForeignKey(**{
        'to': 'users.User',
        'on_delete': models.CASCADE,
        'help_text': 'The user who requested the email change.',
    })
    url = models.UUIDField(**{
        'primary_key': True,
        'default': uuid.uuid4,
        'editable': False,
        'help_text': 'A unique link to confirm the shift.',
    })
    prev_email = models.EmailField(**{
        'max_length': 128,
        'blank': True,
        'editable': False,
        'help_text': 'Current user email.',
    })
    email = models.EmailField(**{
        'max_length': 128,
        'help_text': 'New user email.',
    })
    closed_at = models.DateTimeField(**{
        'default': add_ten_minutes,
        'help_text': 'Duration of the change request.',
    })

    def save(self, *args, **kwargs):
        self.full_clean()
        self.prev_email = self.user.email

        email_is_used = User.objects.filter(**{
            'email': self.email,
        }).exists()

        if email_is_used or self.prev_email == self.email:
            raise ValidationError({
                'email': [
                    'You cannot use this email as a new email.',
                ],
            })

        super().save(*args, **kwargs)
