from typing import List

from graphql_sync_dataloaders import SyncDataLoader

from ..models.Teacher import Teacher


class TeacherLoader(SyncDataLoader):
    def __init__(self):
        super().__init__(teacher_loader)


def teacher_loader(keys: List[int]) -> List[Teacher]:
    teachers = Teacher.objects.select_related('user').filter(**{
        'id__in': keys,
    })
    teacher_map = {teacher.id: teacher for teacher in teachers}

    return [teacher_map.get(key, None) for key in keys]
