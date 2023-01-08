from collections import defaultdict

from graphql_sync_dataloaders import SyncDataLoader

from courses.models.Course import Course
from users.models.Teacher import Teacher


class Loaders:
    def __init__(self):
        self.user_loader = SyncDataLoader(generate_loader_by_foreign_key)
        self.teacher_by_course = SyncDataLoader(batch_teacher_by_course_loader)


def generate_loader_by_foreign_key(keys):
    results_by_ids = defaultdict(list)
    lookup = {'category_id__in': keys}

    data = Course.objects.filter(**lookup).iterator()

    for result in data:
        results_by_ids[getattr(result, 'category_id')].append(result)

    return [results_by_ids.get(id, []) for id in keys]


def batch_teacher_by_course_loader(keys):
    results_by_ids = defaultdict(list)
    lookup = {'id__in': keys}

    data = Teacher.objects \
        .select_related('user') \
        .filter(**lookup) \
        .values('id', 'photo') \
        .iterator()

    for result in data:
        results_by_ids[result.get('id')].append(Teacher(**result))

    return [results_by_ids.get(key, []) for key in keys]
