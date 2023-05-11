from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction

from courses.models.UserCourse import UserCourse


@shared_task(base=Singleton)
def create_user_course_task(course_id: int, user_id: int):
    with transaction.atomic(using='master'):
        UserCourse.objects.create(**{
            'course_id': course_id,
            'user_id': user_id,
        })
