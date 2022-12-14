from django.db import models

from .User import User


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='teachers/%Y/%m/%d/')
    description = models.CharField(max_length=255)
    average_rating = models.DecimalField(max_digits=2, decimal_places=1,
                                         default=0)
    count_graduates = models.PositiveIntegerField(default=0)
    facebook = models.CharField(max_length=255, default='', blank=True)
    twitter = models.CharField(max_length=255, default='', blank=True)
    google_plus = models.CharField(max_length=255, default='', blank=True)
    vk = models.CharField(max_length=255, default='', blank=True)

    class Meta:
        abstract = False

    def __str__(self):
        return f'{self.user}'

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)
