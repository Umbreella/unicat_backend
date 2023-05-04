from django.db import models


class CommentedTypeChoices(models.IntegerChoices):
    COURSE = 0, 'Курс'
    NEWS = 1, 'Новость'
    EVENT = 2, 'Мероприятие'
