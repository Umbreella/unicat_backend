from django.db import models


class QuestionTypeChoices(models.IntegerChoices):
    RADIOBUTTON = 1, 'Один вариант'
    CHECKBOX = 2, 'Несколько вариантов'
    FREE = 3, 'Свободный ответ'
