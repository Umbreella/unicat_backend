from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
