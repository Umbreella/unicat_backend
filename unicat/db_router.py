
class PrimaryDataBaseRouter:
    def db_for_read(self, model, **hints):
        return 'slave'

    def db_for_write(self, model, **hints):
        return 'master'

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {'master', 'slave'}

        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True

        return None

    # def allow_migrate(self, db, app_label, model_name=None, **hints):
    #     print(db)
    #     print(app_label)
    #     print(model_name)
    #     print(hints)
    #
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
