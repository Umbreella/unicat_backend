from courses.models.CourseBody import CourseBody
from courses.models.CourseStat import CourseStat
from lessons.models.LessonBody import LessonBody
from lessons.models.Question import Question
from users.models import User


class PrimaryDataBaseRouter:
    def db_for_read(self, model, **hints):
        instance = hints.get('instance', None)

        read_from_master = (
            CourseBody, CourseStat, LessonBody, Question,
        )

        if isinstance(instance, read_from_master):
            return 'master'

        if isinstance(model, User):
            return 'master'

        return 'slave'

    def db_for_write(self, model, **hints):
        return 'master'

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {'master', 'slave'}

        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True

        return None

    # def allow_migrate(self, db, app_label, model_name=None, **hints):
    #     return False


class TestDataBaseRouter:
    def db_for_read(self, model, **hints):
        return 'master'

    def db_for_write(self, model, **hints):
        return 'master'

    # def allow_relation(self, obj1, obj2, **hints):
    #     db_set = {'primary', 'replica1', 'replica2'}
    #
    #     if obj1._state.db in db_set and obj2._state.db in db_set:
    #         return True
    #
    #     return None
    #
    # def allow_migrate(self, db, app_label, model_name=None, **hints):
    #     return True
