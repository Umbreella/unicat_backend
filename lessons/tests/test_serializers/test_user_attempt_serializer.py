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
from ...serializers.UserAttemptSerializer import UserAttemptSerializer


class UserAttemptSerializerTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserAttemptSerializer

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
            'discount': None,
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
            'lesson_type': LessonTypeChoices.TEST,
            'count_questions': 50,
        })

        Lesson.objects.create(**{
            'id': 2,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY,
        })

        Lesson.objects.create(**{
            'id': 3,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME,
        })

        UserCourse.objects.create(**{
            'course': course,
            'user': user,
        })

        #   'TGVzc29uVHlwZTox' - 'LessonType:1'
        #   'TGVzc29uVHlwZToy' - 'LessonType:2'
        cls.data = {
            'lesson_id': 1,
        }

        cls.context = {
            'user': user,
        }

    def test_Should_IncludeDefiniteFields(self):
        expected_fields = [
            'id', 'time_end', 'count_answered_questions', 'lesson_id',
        ]
        real_fields = list(self.tested_class().get_fields())

        self.assertEqual(expected_fields, real_fields)

    def test_When_DataIsEmpty_Should_ErrorRequiredFields(self):
        context = self.context

        serializer = self.tested_class(data={}, context=context)

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

    def test_When_LessonTypeIsTheme_Should_ErrorValidLessonType(self):
        context = self.context
        data = self.data
        data.update({
            'lesson_id': 3,
        })

        serializer = self.tested_class(data=data, context=context)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'lesson_id': [
                ErrorDetail(**{
                    'string': (
                        'You can not create attempt for this type lesson.'
                    ),
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_LessonTypeIsTheory_Should_ErrorValidLessonType(self):
        context = self.context
        data = self.data
        data.update({
            'lesson_id': 2,
        })

        serializer = self.tested_class(data=data, context=context)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'lesson_id': [
                ErrorDetail(**{
                    'string': (
                        'You can not create attempt for this type lesson.'
                    ),
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_LessonTypeIsTest_Should_CreateNewAttempt(self):
        context = self.context
        data = self.data

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()
        serializer.save()

        expected_raise = {
            'id': 'VXNlckF0dGVtcHRUeXBlOjE=',
            'time_end': None,
            'count_answered_questions': 0,
        }
        real_raise = serializer.data

        self.assertEqual(expected_raise, real_raise)
