from typing import List

from graphql_sync_dataloaders import SyncDataLoader

from ..models.Course import Course


class CertificateTitleLoader(SyncDataLoader):
    def __init__(self):
        super().__init__(certificate_title_loader)


def certificate_title_loader(keys: List[int]) -> List[str]:
    courses = Course.objects.filter(**{
        'id__in': keys,
    })
    course_map = {course.id: course.title for course in courses}

    return [course_map.get(key, None) for key in keys]
