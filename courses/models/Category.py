from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=128, default='')

    class Meta:
        abstract = False

    def __str__(self):
        return f'{self.title}'
