from django.db import models
from django.utils import timezone


class New(models.Model):
    preview = models.ImageField(**{
        'upload_to': 'news/%Y/%m/%d/',
        'help_text': 'News image.',
    })
    title = models.CharField(**{
        'max_length': 255,
        'default': '',
        'help_text': 'News name.',
    })
    short_description = models.CharField(**{
        'max_length': 255,
        'default': '',
        'help_text': 'A brief description of the news displayed on the icon.',
    })
    description = models.TextField(**{
        'help_text': 'Full description of the news.',
    })
    author = models.ForeignKey(**{
        'to': 'users.User',
        'on_delete': models.SET_NULL,
        'null': True,
        'help_text': 'The user who created the news.',
    })
    created_at = models.DateTimeField(**{
        'default': timezone.now,
        'help_text': 'News creation time.',
    })

    class Meta:
        abstract = False

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)
