from django.db import models

from .User import User


class Teacher(models.Model):
    user = models.OneToOneField(**{
        'to': User,
        'on_delete': models.CASCADE,
        'help_text': 'User for whom the teacher record is added.',
    })
    description = models.CharField(**{
        'max_length': 255,
        'help_text': 'Some words about teacher.',
    })
    avg_rating = models.DecimalField(**{
        'max_digits': 2,
        'decimal_places': 1,
        'default': 0,
        'help_text': 'Average rating from all teachers courses.',
    })
    count_reviews = models.PositiveIntegerField(**{
        'default': 0,
        'help_text': (
            'The total number of all reviews left by users for all courses '
            'of this teacher.'
        ),
    })
    facebook = models.CharField(**{
        'max_length': 255,
        'default': '',
        'blank': True,
        'help_text': 'Link to the user`s Facebook page.',
    })
    twitter = models.CharField(**{
        'max_length': 255,
        'default': '',
        'blank': True,
        'help_text': 'Link to the user`s Twitter page.',
    })
    google_plus = models.CharField(**{
        'max_length': 255,
        'default': '',
        'blank': True,
        'help_text': 'Link to the user`s GooglePlus page.',
    })
    vk = models.CharField(**{
        'max_length': 255,
        'default': '',
        'blank': True,
        'help_text': 'Link to the user`s VK page.',
    })

    def __str__(self):
        return f'{self.user}'

    def save(self, *args, **kwargs):
        if isinstance(self.avg_rating, float):
            self.avg_rating = round(self.avg_rating, 1)

        self.full_clean()
        super().save(*args, **kwargs)
