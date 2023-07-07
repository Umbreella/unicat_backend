from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction


@shared_task(base=Singleton)
def update_course_count_listeners_task(course_id: int):
    from ..models.Course import Course
    from ..models.UserCourse import UserCourse

    with transaction.atomic(using='master'):
        count_listeners = UserCourse.objects.using('master').filter(**{
            'course_id': course_id,
        }).count()

        Course.objects.filter(**{
            'id': course_id,
        }).update(**{
            'count_listeners': count_listeners,
        })

        return 'Course count_listeners is updated.'
