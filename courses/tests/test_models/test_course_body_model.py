from django.core.exceptions import ValidationError as DjValidationError
from django.db.models import BigAutoField, OneToOneField, TextField
from django.test import TestCase

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.CourseBody import CourseBody
from ...models.LearningFormat import LearningFormat


class CourseBodyModelTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CourseBody

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

        cls.data = {
            'course': course,
            'body': 'q' * 64,
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'id', 'course', 'body',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'course': OneToOneField,
            'body': TextField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'id': '',
            'course': 'The course for which you need to create its content.',
            'body': 'Course content displayed on the Description tab.',
        }
        real_help_text = {
            field.name: field.help_text
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreateCourseBodyWithOutData_Should_ErrorBlankField(self):
        course_body = self.tested_class()

        with self.assertRaises(DjValidationError) as _raise:
            course_body.save()

        expected_raise = {
            'body': [
                'This field cannot be blank.',
            ],
            'course': [
                'This field cannot be null.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SaveCourseStatWithDefaultValues(self):
        data = self.data

        course_body = self.tested_class(**data)
        course_body.save()

        expected_str = f'{course_body.course} - {course_body.body[:50]}'
        real_str = str(course_body)

        self.assertEqual(expected_str, real_str)
