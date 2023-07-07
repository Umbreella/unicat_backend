from typing import List

from graphql_sync_dataloaders import SyncDataLoader

from ..models.Lesson import Lesson
from ..models.LessonTypeChoices import LessonTypeChoices


class PublicChildrenLessonLoader(SyncDataLoader):
    def __init__(self):
        super().__init__(public_children_lesson_loader)


def public_children_lesson_loader(keys: List[int]) -> List[List[Lesson]]:
    lessons = Lesson.objects.select_related('parent').filter(**{
        'parent_id__in': keys,
        'lesson_type__in': [
            LessonTypeChoices.THEORY.value,
            LessonTypeChoices.THEME.value,
        ],
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
