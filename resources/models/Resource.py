import os
import uuid

from django.db import models
from django.utils import timezone


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    dir_path = timezone.now().strftime('resources/%Y/%m/%d/')

    return os.path.join(dir_path, filename)


class Resource(models.Model):
    name = models.CharField(max_length=255)
    file = models.ImageField(upload_to=get_file_path)
    loaded_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        os.remove(self.file.path)
        super().delete(*args, **kwargs)
