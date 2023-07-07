from django.core.exceptions import ValidationError
from django.db.models import BigAutoField, OneToOneField, TextField
from django.test import TestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonBody import LessonBody
from ...models.LessonTypeChoices import LessonTypeChoices


class LessonBodyTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LessonBody

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

        lesson = Lesson.objects.create(**{
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY,
        })

        cls.data = {
            'lesson': lesson,
            'body': 'q' * 50,
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'id', 'lesson', 'body',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'lesson': OneToOneField,
            'body': TextField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'body': 'Full content of the lesson.',
            'id': '',
            'lesson': 'The lesson to which the full content refers.',
        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }
        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreateLessonBodyWithOutData_Should_ErrorBlankFields(self):
        lesson_body = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            lesson_body.save()

        expected_raise = {
            'lesson': [
                'This field cannot be null.',
            ],
            'body': [
                'This field cannot be blank.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_CreateLessonWithRequiredData_Should_SaveLessonBody(self):
        data = self.data

        lesson_body = self.tested_class(**data)
        lesson_body.save()

        expected_dict = {
            'id': 1,
            'lesson_id': 1,
            'body': 'q' * 50,
        }
        real_dict = dict(lesson_body)

        self.assertEqual(expected_dict, real_dict)
