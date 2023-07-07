from django.test import TestCase
from graphql_sync_dataloaders import SyncDataLoader

from ...loaders.TeacherLoader import TeacherLoader, teacher_loader
from ...models import User
from ...models.Teacher import Teacher


class TeacherLoaderTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = TeacherLoader
        cls.batch_load_fn = teacher_loader

        first_user = User.objects.create(**{
            'id': 1,
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        second_user = User.objects.create(**{
            'id': 2,
            'email': 'w' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        third_user = User.objects.create(**{
            'id': 3,
            'email': 'e' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        Teacher.objects.create(**{
            'id': 4,
            'user': first_user,
            'description': 'q' * 50,
        })

        Teacher.objects.create(**{
            'id': 5,
            'user': second_user,
            'description': 'q' * 50,
        })

        Teacher.objects.create(**{
            'id': 6,
            'user': third_user,
            'description': 'q' * 50,
        })

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
        keys = [1, 3, 5, ]

        expected_data = [
            None, None,
            *list(Teacher.objects.filter(**{
                'id__in': keys,
            })),
        ]
        real_data = self.batch_load_fn(keys)

        self.assertEqual(expected_data, real_data)
