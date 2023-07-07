from django.test import TestCase
from graphql_sync_dataloaders import SyncDataLoader

from ...loaders.CategoryLoader import CategoryLoader, category_loader
from ...models.Category import Category


class CategoryLoaderTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CategoryLoader
        cls.batch_load_fn = category_loader

        Category.objects.create(**{
            'id': 1,
            'title': 'q' * 50,
        })

        Category.objects.create(**{
            'id': 2,
            'title': 'w' * 50,
        })

        Category.objects.create(**{
            'id': 3,
            'title': 'e' * 50,
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
            *list(Category.objects.filter(**{
                'id__in': keys,
            })),
            None,
        ]
        real_data = self.batch_load_fn(keys)

        self.assertEqual(expected_data, real_data)
