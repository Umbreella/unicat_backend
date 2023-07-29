from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction
from django.db.models import Avg, Sum

from users.models.Teacher import Teacher


@shared_task(base=Singleton)
def update_teacher_info_task(teacher_id: int):
    from ..models.Course import Course
    from ..models.CourseStat import CourseStat

    with transaction.atomic(using='master'):
        all_course_by_teacher = Course.objects.using('master').filter(**{
            'teacher_id': teacher_id,
        }).values_list('id', flat=True)

        avg_rating = Course.objects.using('master').filter(**{
            'id__in': all_course_by_teacher,
        }).aggregate(**{
            'avg_rating': Avg('avg_rating'),
        }).get('avg_rating')

        count_reviews = CourseStat.objects.using('master').filter(**{
            'course_id__in': all_course_by_teacher,
        }).aggregate(**{
            'count_reviews': Sum('count_comments'),
        }).get('count_reviews')

        teacher = Teacher.objects.using('master').get(**{
            'id': teacher_id,
        })

        teacher.avg_rating = avg_rating
        teacher.count_reviews = count_reviews
        teacher.save()

        return 'Teacher info is updated.'
