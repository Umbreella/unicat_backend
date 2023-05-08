from django.core.exceptions import ValidationError
from django.db.models import BigAutoField, BooleanField, CharField, ForeignKey
from django.test import TestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.AnswerValue import AnswerValue
from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.Question import Question
from ...models.QuestionTypeChoices import QuestionTypeChoices


class AnswerValueTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = AnswerValue

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

        lesson = Lesson.objects.create(**{
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY,
        })

        question = Question.objects.create(**{
            'lesson': lesson,
            'body': 'q' * 50,
            'question_type': QuestionTypeChoices.RADIOBUTTON,
        })

        cls.data = {
            'question': question,
            'value': 'q' * 50,
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'id', 'question', 'value', 'is_true',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'question': ForeignKey,
            'value': CharField,
            'is_true': BooleanField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_When_CreateAnswerValueWithOutData_Should_ErrorBlankFields(self):
        answer_value = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            answer_value.save()

        expected_raise = {
            'question': [
                'This field cannot be null.',
            ],
            'value': [
                'This field cannot be blank.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_LengthDataGreaterThan128_Should_ErrorMaxLengthFields(self):
        data = self.data
        data.update({
            'value': 'q' * 129,
        })

        answer_value = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            answer_value.save()

        expected_raise = {
            'value': [
                'Ensure this value has at most 128 characters (it has 129).'
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_CreateAnswerValueWithValidData_Should_SaveAnswerValue(self):
        data = self.data

        answer_value = self.tested_class(**data)
        answer_value.save()

        real_is_true = answer_value.is_true

        self.assertTrue(real_is_true)
