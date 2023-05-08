from django.core.exceptions import ValidationError
from django.db.models import (BigAutoField, CharField, DurationField,
                              ForeignKey, ManyToManyField, ManyToOneRel,
                              OneToOneRel, PositiveSmallIntegerField)
from django.test import TestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices


class LessonTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Lesson

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

        cls.course = Course.objects.create(**{
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

        cls.data = {
            'course': cls.course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY,
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'children', 'questions', 'lesson_body', 'progress',
            'id', 'course', 'serial_number', 'parent', 'title', 'description',
            'lesson_type', 'time_limit', 'count_questions', 'listeners',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'children': ManyToOneRel,
            'questions': ManyToOneRel,
            'lesson_body': OneToOneRel,
            'progress': ManyToOneRel,
            'id': BigAutoField,
            'course': ForeignKey,
            'serial_number': PositiveSmallIntegerField,
            'parent': ForeignKey,
            'title': CharField,
            'description': CharField,
            'lesson_type': PositiveSmallIntegerField,
            'time_limit': DurationField,
            'count_questions': PositiveSmallIntegerField,
            'listeners': ManyToManyField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_When_CreateLessonWithOutData_Should_ErrorBlankFields(self):
        lesson = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            lesson.save()

        expected_raise = {
            'course': [
                'This field cannot be null.',
            ],
            'description': [
                'This field cannot be blank.',
            ],
            'lesson_type': [
                'This field cannot be null.',
            ],
            'title': [
                'This field cannot be blank.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_LengthDataGreaterThan255_Should_ErrorMaxLengthField(self):
        data = self.data
        data.update({
            'description': 'q' * 256,
            'title': 'q' * 256,
        })

        lesson = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            lesson.save()

        expected_raise = {
            'description': [
                'Ensure this value has at most 255 characters (it has 256).'],
            'title': [
                'Ensure this value has at most 255 characters (it has 256).'],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_CreateLessonWithRequiredData_Should_SaveLesson(self):
        data = self.data

        lesson = self.tested_class(**data)
        lesson.save()
        self.course.refresh_from_db()

        expected_dict = {
            'count_questions': 0,
            'course_id': 1,
            'description': 'q' * 50,
            'id': 1,
            'lesson_type': 2,
            'parent_id': None,
            'serial_number': 1,
            'time_limit': None,
            'title': 'q' * 50,
        }
        real_dict = dict(lesson)

        expected_count_lectures = 1
        real_count_lectures = self.course.count_lectures

        self.assertEqual(expected_dict, real_dict)
        self.assertEqual(expected_count_lectures, real_count_lectures)
