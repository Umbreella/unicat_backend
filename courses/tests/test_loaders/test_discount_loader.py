from datetime import timedelta

from django.db import connections
from django.test import TestCase
from django.utils import timezone
from django.utils.connection import ConnectionProxy
from graphql_sync_dataloaders import SyncDataLoader

from users.models import User
from users.models.Teacher import Teacher

from ...loaders.DiscountLoader import DiscountLoader, discount_loader
from ...models.Category import Category
from ...models.Course import Course
from ...models.Discount import Discount
from ...models.LearningFormat import LearningFormat


class DiscountLoaderTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = DiscountLoader
        cls.batch_load_fn = discount_loader

        user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': user,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        Course.objects.create(**{
            'id': 1,
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        Course.objects.create(**{
            'id': 2,
            'teacher': teacher,
            'title': 'w' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        Course.objects.create(**{
            'id': 3,
            'teacher': teacher,
            'title': 'e' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        with ConnectionProxy(connections, 'master').cursor() as c:
            c.execute("""
            INSERT INTO courses_discount(
                id,
                course_id,
                percent,
                start_date,
                end_date
            )
            VALUES (4, 1, 5, '%s', '%s');
            """ % (
                timezone.now() - timedelta(days=5),
                timezone.now() + timedelta(days=5),
            ))
            c.execute("""
            INSERT INTO courses_discount(
                id,
                course_id,
                percent,
                start_date,
                end_date
            )
            VALUES (5, 2, 10, '%s', '%s');
            """ % (
                timezone.now() + timedelta(days=10),
                timezone.now() + timedelta(days=20),
            ))

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
            *list(Discount.objects.filter(**{
                'course_id__in': keys,
                'start_date__lte': timezone.now(),
                'end_date__gte': timezone.now(),
            })),
            None, None,
        ]
        real_data = self.batch_load_fn(keys)

        self.assertEqual(expected_data, real_data)
