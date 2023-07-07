from django.test import TestCase
from graphql_sync_dataloaders import SyncDataLoader

from users.models import User
from users.models.Teacher import Teacher

from ...loaders.UserProgressLoader import (UserProgressLoader, get_progress,
                                           user_progress_loader)
from ...models.Category import Category
from ...models.Course import Course
from ...models.LearningFormat import LearningFormat
from ...models.UserCourse import UserCourse


class UserProgressLoaderTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserProgressLoader
        cls.batch_load_fn = user_progress_loader

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

        first_course = Course.objects.create(**{
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

        UserCourse.objects.create(**{
            'id': 4,
            'course': first_course,
            'user': user,
            'count_lectures_completed': 10,
            'count_independents_completed': 10,
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
        course_ids = (1, 3, 5,)
        user_ids = (1, 2, 3,)

        keys = [(course_ids[i], user_ids[i],) for i in range(3)]

        user_courses = [
            UserCourse.objects.select_related('course').filter(**{
                'course_id': course_ids[i],
                'user_id': user_ids[i],
            }).first() for i in range(3)
        ]

        expected_data = [
            get_progress(user_course) for user_course in user_courses
        ]
        real_data = self.batch_load_fn(keys)

        self.assertEqual(expected_data, real_data)
