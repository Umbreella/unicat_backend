from datetime import timedelta

from django.core.cache import cache
from django.db import connections
from django.test import TestCase
from django.utils import timezone
from django.utils.connection import ConnectionProxy
from rest_framework.exceptions import ErrorDetail, ValidationError

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.UserAttempt import UserAttempt
from ...models.UserLesson import UserLesson
from ...serializers.UserAttemptRefreshSerializer import \
    UserAttemptRefreshSerializer
from ...serializers.UserAttemptSerializer import UserAttemptSerializer


class UserAttemptRefreshSerializerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserAttemptRefreshSerializer

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

        course = Course.objects.create(**{
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

        first_lesson = Lesson.objects.create(**{
            'id': 1,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST,
            'count_questions': 50,
            'time_limit': timedelta(days=1),
        })

        UserLesson.objects.create(**{
            'id': 1,
            'user': user,
            'lesson': first_lesson,
        })

        with ConnectionProxy(connections, 'master').cursor() as c:
            c.execute("""
            INSERT INTO lessons_userattempt(
                id,
                time_start,
                time_end,
                count_true_answer,
                user_lesson_id
            )
            VALUES (1, '%s', '%s', 0, 1);
            """ % (
                timezone.now() - timedelta(days=2),
                timezone.now() - timedelta(days=1),
            ))
            c.execute("""
            INSERT INTO lessons_userattempt(
                id,
                time_start,
                time_end,
                count_true_answer,
                user_lesson_id
            )
            VALUES (2, '%s', '%s', 0, 1);
            """ % (
                timezone.now() - timedelta(days=1),
                timezone.now() + timedelta(days=1),
            ))
            c.execute("""
            INSERT INTO lessons_userattempt(
                id,
                time_start,
                time_end,
                count_true_answer,
                user_lesson_id
            )
            VALUES (3, '%s', null, 0, 1);
            """ % (
                timezone.now() - timedelta(days=1),
            ))

        cls.data = {
            'lesson_id': 1,
        }

        cls.context = {
            'user': user,
        }

    @classmethod
    def setUp(cls):
        cache.clear()

    @classmethod
    def tearDown(cls):
        cache.clear()

    def test_Should_InheritModelSerializer(self):
        expected_super_classes = (
            UserAttemptSerializer,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_IncludeDefiniteFields(self):
        expected_fields = list(UserAttemptSerializer().get_fields())
        real_fields = list(self.tested_class().get_fields())

        self.assertEqual(expected_fields, real_fields)

    def test_Should_DontOverrideSuperMethodValidate(self):
        expected_method = UserAttemptSerializer.validate
        real_method = self.tested_class.validate

        self.assertEqual(expected_method, real_method)

    def test_Should_DontOverrideSuperMethodCreate(self):
        expected_method = UserAttemptSerializer.create
        real_method = self.tested_class.create

        self.assertEqual(expected_method, real_method)

    def test_When_DataIsEmpty_Should_ErrorRequiredFields(self):
        serializer = self.tested_class(data={}, context=self.context)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'lesson_id': [
                ErrorDetail(**{
                    'string': 'This field is required.',
                    'code': 'required',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllAttemptsIsEnded_Should_ErrorActiveAttemptIsNotFound(self):
        UserAttempt.objects.filter(**{
            'id__in': [2, 3, ],
        }).delete()

        data = self.data

        serializer = self.tested_class(data=data, context=self.context)
        serializer.is_valid()

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'lesson_id': [
                ErrorDetail(**{
                    'string': 'Active attempt is not found.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_AttemptEndInFuture_Should_CreateNewUserAttempt(self):
        UserAttempt.objects.filter(**{
            'id__in': [3, ],
        }).delete()
        data = self.data

        serializer = self.tested_class(data=data, context=self.context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        expected_instance = None
        real_instance = serializer.save()

        expected_attempt = UserAttempt.objects.last()
        real_attempt = real_instance

        self.assertNotEqual(expected_instance, real_instance)
        self.assertEqual(expected_attempt, real_attempt)

    def test_When_AttemptEndInNull_Should_CreateNewUserAttempt(self):
        UserAttempt.objects.filter(**{
            'id__in': [2, ],
        }).delete()
        data = self.data

        serializer = self.tested_class(data=data, context=self.context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        expected_instance = None
        real_instance = serializer.save()

        expected_attempt = UserAttempt.objects.last()
        real_attempt = real_instance

        self.assertNotEqual(expected_instance, real_instance)
        self.assertEqual(expected_attempt, real_attempt)
