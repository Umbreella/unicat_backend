import uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone


def add_ten_minutes():
    return timezone.now() + timedelta(minutes=10)


class ChangeEmail(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    url = models.UUIDField(primary_key=True, default=uuid.uuid4,
                           editable=False)
    email = models.EmailField(max_length=128)
    closed_at = models.DateTimeField(default=add_ten_minutes)
