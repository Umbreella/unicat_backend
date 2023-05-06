from django.db import models
from django.utils import timezone


class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=128)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_closed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
