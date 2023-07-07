from typing import List

from graphql_sync_dataloaders import SyncDataLoader

from ..models.CourseBody import CourseBody


class CourseBodyLoader(SyncDataLoader):
    def __init__(self):
        super().__init__(course_body_loader)


def course_body_loader(keys: List[int]) -> List[CourseBody]:
    course_bodies = CourseBody.objects.filter(**{
        'course_id__in': keys,
    })
    course_body = {body.course_id: body.body for body in course_bodies}

    return [course_body.get(key, None) for key in keys]
