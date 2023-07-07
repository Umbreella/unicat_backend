from typing import List, Tuple

from graphql_sync_dataloaders import SyncDataLoader

from ..models.UserCourse import UserCourse


class UserProgressLoader(SyncDataLoader):
    def __init__(self):
        super().__init__(user_progress_loader)


def user_progress_loader(keys: List[Tuple[int, int]]) -> List[float]:
    course_keys = set()
    user_keys = set()

    for course, user in keys:
        course_keys.add(course)
        user_keys.add(user)

    user_courses = UserCourse.objects.select_related('course').filter(**{
        'course_id__in': course_keys,
        'user_id__in': user_keys,
    })
    user_course_map = {
        (course.course_id, course.user_id,): get_progress(course)
        for course in user_courses
    }

    return [user_course_map.get(key, None) for key in keys]


def get_progress(user_course: UserCourse) -> float:
    if not user_course:
        return None

    count_lessons = sum([
        user_course.course.count_lectures,
        user_course.course.count_independents,
    ])

    count_completed_lessons = sum([
        user_course.count_lectures_completed,
        user_course.count_independents_completed,
    ])

    progress = count_completed_lessons / count_lessons

    return round(progress * 100, 3)
