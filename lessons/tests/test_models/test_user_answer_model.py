from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models import BigAutoField, BooleanField, ForeignKey
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
from ...models.UserAnswer import UserAnswer
from ...models.UserAttempt import UserAttempt
from ...models.UserLesson import UserLesson


class UserAnswerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserAnswer

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
            'lesson_type': LessonTypeChoices.TEST,
            'count_questions': 10,
        })

        question = Question.objects.create(**{
            'id': 1,
            'lesson': lesson,
            'body': 'q' * 50,
            'question_type': QuestionTypeChoices.RADIOBUTTON,
        })

        user_lesson = UserLesson.objects.create(**{
            'lesson': lesson,
            'user': user,
        })

        user_attempt = UserAttempt.objects.create(**{
            'id': 1,
            'user_lesson': user_lesson,
        })

        cls.data = {
            'user_attempt': user_attempt,
            'question': question,
        }

        cls.cache_key = 'VXNlckF0dGVtcHRUeXBlOjE=_answered_questions'

    @classmethod
    def setUp(cls):
        cache.clear()

    @classmethod
    def tearDown(cls):
        cache.clear()

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'id', 'user_attempt', 'question', 'is_true',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'user_attempt': ForeignKey,
            'question': ForeignKey,
            'is_true': BooleanField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'id': '',
            'is_true': 'Is this answer correct.',
            'question': 'The question to which this answer refers.',
            'user_attempt': 'The user attempt to which this response refers.',
        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreateUserAnswerWithOutData_Should_ErrorBlankFields(self):
        user_answer = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            user_answer.save()

        expected_raise = {
            'user_attempt': [
                'This field cannot be null.',
            ],
            'question': [
                'This field cannot be null.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_CreateUserAnswerWithValidData_Should_SaveUserAnswer(self):
        data = self.data

        user_answer = self.tested_class(**data)
        user_answer.save()

        expected_dict = {
            'id': 1,
            'is_true': False,
            'question_id': 1,
            'user_attempt_id': 1,
        }
        real_dict = dict(user_answer)

        self.assertEqual(expected_dict, real_dict)

    def test_When_CreateDuplicateUserAnswer_Should_ErrorNotUniqueFields(self):
        data = self.data

        user_answer = self.tested_class(**data)
        user_answer.save()

        user_answer_duplicate = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            user_answer_duplicate.save()

        expected_raise = {
            '__all__': [
                (
                    'User answer with this User attempt and Question already '
                    'exists.'
                ),
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_CreateUserAnswerIsTrue_Should_UpdateUserAttempt(self):
        data = self.data
        data.update({
            'is_true': True,
        })

        user_answer = self.tested_class(**data)
        user_answer.save()

        expected_count_true_answer = 1
        real_count_true_answer = user_answer.user_attempt.count_true_answer

        expected_cache_value = [1, ]
        real_cache = cache.get(self.cache_key)

        self.assertEqual(expected_count_true_answer, real_count_true_answer)
        self.assertEqual(expected_cache_value, real_cache)

    def test_When_CreateUserAnswerIsFalse_Should_DontUpdateUserAttempt(self):
        data = self.data
        data.update({
            'is_true': False,
        })

        user_answer = self.tested_class(**data)
        user_answer.save()

        expected_count_true_answer = 0
        real_count_true_answer = user_answer.user_attempt.count_true_answer

        expected_cache_value = [1, ]
        real_cache = cache.get(self.cache_key)

        self.assertEqual(expected_count_true_answer, real_count_true_answer)
        self.assertEqual(expected_cache_value, real_cache)
