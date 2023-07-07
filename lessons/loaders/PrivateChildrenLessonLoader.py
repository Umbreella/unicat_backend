from typing import List

from graphql_sync_dataloaders import SyncDataLoader

from ..models.Lesson import Lesson


class PrivateChildrenLessonLoader(SyncDataLoader):
    def __init__(self):
        super().__init__(private_children_lesson_loader)


def private_children_lesson_loader(keys: List[int]) -> List[List[Lesson]]:
    lessons = Lesson.objects.select_related('parent').filter(**{
        'parent_id__in': keys,
    }).order_by('serial_number')

    lesson_map = {}
    for lesson in lessons:
        children = lesson_map.get(lesson.parent_id)

        if not children:
            children = [lesson, ]
        else:
            children.append(lesson)

        lesson_map[lesson.parent_id] = children

    return [lesson_map.get(key, []) for key in keys]
