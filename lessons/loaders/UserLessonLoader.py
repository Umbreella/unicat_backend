from typing import List, Tuple

from graphql_sync_dataloaders import SyncDataLoader

from ..models.UserLesson import UserLesson


class UserLessonLoader(SyncDataLoader):
    def __init__(self):
        super().__init__(user_lesson_loader)


def user_lesson_loader(keys: List[Tuple[int, int]]) -> List[bool]:
    lesson_ids = set()
    user_ids = set()

    for lesson, user in keys:
        lesson_ids.add(lesson)
        user_ids.add(user)

    user_lessons = UserLesson.objects.filter(**{
        'lesson_id__in': lesson_ids,
        'user_id__in': user_ids,
    })

    user_lesson_map = {
        (lesson.lesson_id, lesson.user_id,): bool(lesson.completed_at)
        for lesson in user_lessons
    }

    return [user_lesson_map.get(key, False) for key in keys]
