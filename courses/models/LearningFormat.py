from django.db import models


class LearningFormat(models.IntegerChoices):
    REMOTE = 1, 'Дистанционно'
    FULL_TIME = 2, 'Очно'
    FULL_PART_TIME = 3, 'Очно-заочно'
