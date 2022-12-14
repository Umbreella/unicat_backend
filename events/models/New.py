from datetime import datetime

from django.db import models


class New(models.Model):
    preview = models.ImageField(upload_to='news/%Y/%m/%d/')
    title = models.CharField(max_length=255, default='')
    short_description = models.CharField(max_length=255, default='')
    description = models.TextField()
    author = models.ForeignKey('users.User', on_delete=models.SET_NULL,
                               null=True)
    created_at = models.DateField(default=datetime.now)

    class Meta:
        abstract = False

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)
