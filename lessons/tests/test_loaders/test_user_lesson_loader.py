from django.test import TestCase
from graphql_sync_dataloaders import SyncDataLoader

from ...loaders.UserLessonLoader import UserLessonLoader, user_lesson_loader


class UserLessonLoaderTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserLessonLoader
        cls.batch_load_fn = user_lesson_loader

    def test_Should_InheritSyncDataLoader(self):
        expected_super_classes = (
            SyncDataLoader,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_OverrideSuperMethodInit(self):
        expected_method = SyncDataLoader.__init__
        real_method = self.tested_class.__init__

        self.assertNotEqual(expected_method, real_method)

    def test_Should_SetUpBatchLoadFN(self):
        expected_method = self.batch_load_fn
        real_method = self.tested_class()._batch_load_fn

        self.assertEqual(expected_method, real_method)

    def test_When_UseBatchLoadFN_Should_ReturnListOfQuerySet(self):
        keys = [
            (1, 1,), (3, 1,), (5, 1,),
        ]

        expected_data = [
            False, False, False,
        ]
        real_data = self.batch_load_fn(keys)

        self.assertEqual(expected_data, real_data)
