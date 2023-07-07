from django.core.exceptions import ValidationError
from django.db.models import (BigAutoField, CharField, ForeignKey,
                              ManyToOneRel, PositiveSmallIntegerField)
from django.test import TestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.Question import Question
from ...models.QuestionTypeChoices import QuestionTypeChoices


class QuestionTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Question

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

        cls.lesson = Lesson.objects.create(**{
            'id': 1,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST,
            'count_questions': 50,
        })

        cls.data = {
            'lesson': cls.lesson,
            'body': 'q' * 50,
            'question_type': QuestionTypeChoices.RADIOBUTTON,
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'answers', 'user_answers', 'id', 'lesson', 'body', 'question_type',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'answers': ManyToOneRel,
            'user_answers': ManyToOneRel,
            'id': BigAutoField,
            'lesson': ForeignKey,
            'body': CharField,
            'question_type': PositiveSmallIntegerField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'answers': '',
            'body': 'Question body.',
            'id': '',
            'lesson': 'The lesson to which this question relates.',
            'question_type': 'Question type by the number of correct answers.',
            'user_answers': '',
        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreateQuestionWithOutData_Should_ErrorBlankFields(self):
        question = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            question.save()

        expected_raise = {
            'lesson': [
                'This field cannot be null.',
            ],
            'body': [
                'This field cannot be blank.',
            ],
            'question_type': [
                'This field cannot be null.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_CreateQuestionWithLongData_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'body': 'q' * 513,
        })

        question = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            question.save()

        expected_raise = {
            'body': [
                'Ensure this value has at most 512 characters (it has 513).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_CreateQuestionWithRequiredData_Should_SaveQuestion(self):
        data = self.data

        question = self.tested_class(**data)
        question.save()

        expected_dict = {
            'id': 1,
            'lesson_id': 1,
            'body': 'q' * 50,
            'question_type': 1,
        }
        real_dict = dict(question)

        self.assertEqual(expected_dict, real_dict)

    def test_When_SaveQuestion_Should_UpdateCountQuestionInLesson(self):
        data = self.data

        question = self.tested_class(**data)
        question.save()
        self.lesson.refresh_from_db()

        expected_count_question = 1
        real_count_question = self.lesson.count_questions

        self.assertEqual(expected_count_question, real_count_question)

    def test_When_DeleteQuestion_Should_UpdateCountQuestionInLesson(self):
        data = self.data

        question = self.tested_class(**data)
        question.save()
        question.delete()
        self.lesson.refresh_from_db()

        expected_count_question = 0
        real_count_question = self.lesson.count_questions

        self.assertEqual(expected_count_question, real_count_question)
