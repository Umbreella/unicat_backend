from django.db import models


class LessonTypeChoices(models.IntegerChoices):
    THEME = 1, 'Тема'
    THEORY = 2, 'Теория'
    TEST = 3, 'Тест'
