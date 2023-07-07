from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction
from django.utils import timezone

from courses.models.UserCourse import UserCourse


@shared_task(base=Singleton)
def update_user_course_last_view_task(user_course_id: int):
    with transaction.atomic(using='master'):
        UserCourse.objects.filter(**{
            'id': user_course_id
        }).update(**{
            'last_view': timezone.now(),
        })

        return 'UserCourse last_view is updated.'
