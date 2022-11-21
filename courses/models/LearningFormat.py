from django.db import models


class LearningFormat(models.TextChoices):
    REMOTE = 'part', 'Дистанционно'
    FULL_TIME = 'full', 'Очно'
    FULL_PART_TIME = 'both', 'Очно-заочно'
