from django.db import models


class CommentedType(models.TextChoices):
    COURSE = 'course', 'Курс'
    NEWS = 'news', 'Новость'
    EVENT = 'event', 'Мероприятие'
