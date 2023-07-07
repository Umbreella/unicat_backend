from django.test import TestCase
from rest_framework.exceptions import ErrorDetail, ValidationError

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from courses.models.UserCourse import UserCourse
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.UserLesson import UserLesson
from ...serializers.LessonCompleteSerializer import LessonCompleteSerializer


class LessonCompleteSerializerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LessonCompleteSerializer

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

        Lesson.objects.create(**{
            'id': 1,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME,
        })

        Lesson.objects.create(**{
            'id': 2,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST,
        })

        Lesson.objects.create(**{
            'id': 3,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY,
        })

        UserCourse.objects.create(**{
            'course': course,
            'user': user,
        })

        cls.data = {
            'lesson_id': 3,
        }

        cls.context = {
            'user': user,
        }

    def test_Should_IncludeDefiniteFields(self):
        expected_fields = [
            'lesson_id',
        ]
        real_fields = list(self.tested_class().get_fields())

        self.assertEqual(expected_fields, real_fields)

    def test_When_LessonTypeIsTheme_Should_ErrorNotValidLessonType(
            self):
        data = self.data
        context = self.context

        data.update({
            'lesson_id': 1,
        })

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'lesson_id': [
                ErrorDetail(**{
                    'string': 'You can not complete lesson this type.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_LessonTypeIsTest_Should_ErrorNotValidLessonType(
            self):
        data = self.data
        context = self.context

        data.update({
            'lesson_id': 2,
        })

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'lesson_id': [
                ErrorDetail(**{
                    'string': 'You can not complete lesson this type.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_LessonTypeIsTheory_Should_CreateUserLesson(
            self):
        data = self.data
        context = self.context

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()

        expected_instance = None
        real_instance = serializer.save()

        expected_completed_at = None
        real_completed_at = UserLesson.objects.last().completed_at

        self.assertNotEqual(expected_instance, real_instance)
        self.assertNotEqual(expected_completed_at, real_completed_at)

    def test_When_DuplicateLessonComplete_Should_DontUpdateLessonComplete(
            self):
        data = self.data
        context = self.context

        save_serializer = self.tested_class(data=data, context=context)
        save_serializer.is_valid()
        save_serializer.save()

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()
        serializer.save()

        expected_data = save_serializer.data
        real_data = serializer.data

        self.assertEqual(expected_data, real_data)
