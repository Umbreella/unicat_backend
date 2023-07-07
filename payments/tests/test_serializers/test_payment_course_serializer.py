from django.test import TestCase
from rest_framework.exceptions import ErrorDetail, ValidationError

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...serializers.PaymentCourseSerializer import PaymentCourseSerializer


class PaymentCourseSerializerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = PaymentCourseSerializer

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

        cls.data = {
            'course_id': 'Q291cnNlVHlwZTox',
        }

    def test_When_EmptyData_Should_ErrorRequiredFields(self):
        data = {}

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'course_id': [
                ErrorDetail(**{
                    'string': 'This field is required.',
                    'code': 'required',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_EmptyFields_Should_ErrorBlankFields(self):
        data = {
            'course_id': '',
            'password': ''
        }

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'course_id': [
                ErrorDetail(**{
                    'string': 'This field may not be blank.',
                    'code': 'blank',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataLessThanMinLength_Should_ErrorMinLength(self):
        data = {
            'course_id': 'q' * 15,
        }

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'course_id': [
                ErrorDetail(**{
                    'string': (
                        'Ensure this field has at least 16 characters.'
                    ),
                    'code': 'min_length',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataGreaterThanMaxLength_Should_ErrorMaxLength(self):
        data = {
            'course_id': 'q' * 41,
        }

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_errors = {
            'course_id': [
                ErrorDetail(**{
                    'string': (
                        'Ensure this field has no more than 40 characters.'
                    ),
                    'code': 'max_length',
                }),
            ],
        }
        real_errors = _raise.exception.detail

        self.assertEqual(expected_errors, real_errors)

    def test_When_RandomData_Should_ErrorNotBase64(self):
        data = {
            'course_id': 'q' * 16,
        }

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'course_id': [
                ErrorDetail(**{
                    'string': 'Not valid value.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_CourseIdIsNotFound_Should_ErrorNotFound(self):
        data = self.data
        data.update({
            'course_id': 'Q291cnNlVHlwZToy',
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'course_id': [
                ErrorDetail(**{
                    'string': 'This course is not found.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataIsValid_Should_ReturnValidatedDataAndSetAttrCourse(self):
        data = self.data

        serializer = self.tested_class(data=data)
        serializer.is_valid()

        expected_validated_data = {
            'course_id': 1,
        }
        real_validated_data = serializer.validated_data

        expected_course = None
        real_course = serializer.course

        self.assertEqual(expected_validated_data, real_validated_data)
        self.assertNotEqual(expected_course, real_course)
