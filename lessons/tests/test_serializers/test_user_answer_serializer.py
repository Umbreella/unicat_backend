from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import (ErrorDetail, PermissionDenied,
                                       ValidationError)

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from courses.models.UserCourse import UserCourse
from users.models import User
from users.models.Teacher import Teacher

from ...models.AnswerValue import AnswerValue
from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.Question import Question
from ...models.QuestionTypeChoices import QuestionTypeChoices
from ...models.UserAttempt import UserAttempt
from ...models.UserLesson import UserLesson
from ...serializers.UserAnswerSerializer import UserAnswerSerializer


class UserAnswerSerializerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserAnswerSerializer

        user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        cls.user_without_access = User.objects.create_user(**{
            'email': 'w' * 50 + '@q.qq',
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
            'count_questions': 50,
        })

        UserCourse.objects.create(**{
            'user': user,
            'course': course,
        })

        user_lesson = UserLesson.objects.create(**{
            'lesson': lesson,
            'user': user,
        })

        cls.user_attempt = UserAttempt.objects.create(**{
            'id': 1,
            'user_lesson': user_lesson,
            'time_end': timezone.now() + timedelta(minutes=10)
        })

        question_open = Question.objects.create(**{
            'lesson': lesson,
            'body': 'q' * 50,
            'question_type': QuestionTypeChoices.FREE,
        })

        question_choice = Question.objects.create(**{
            'lesson': lesson,
            'body': 'q' * 50,
            'question_type': QuestionTypeChoices.CHECKBOX,
        })

        AnswerValue.objects.create(**{
            'question': question_open,
            'value': 'q' * 50,
            'is_true': True,
        })

        AnswerValue.objects.create(**{
            'question': question_choice,
            'value': 'q' * 50,
            'is_true': True,
        })

        #   'VXNlckF0dGVtcHRUeXBlOjE=' - 'UserAttemptType:1'
        #   'UXVlc3Rpb25UeXBlOjE=' - 'QuestionType:1'
        cls.data_open_question = {
            'attempt_id': 'VXNlckF0dGVtcHRUeXBlOjE=',
            'question_id': 'UXVlc3Rpb25UeXBlOjE=',
            'answer': ['-', ],
        }

        #   'VXNlckF0dGVtcHRUeXBlOjE=' - 'UserAttemptType:1'
        #   'UXVlc3Rpb25UeXBlOjI=' - 'QuestionType:2'
        cls.data_choice_question = {
            'attempt_id': 'VXNlckF0dGVtcHRUeXBlOjE=',
            'question_id': 'UXVlc3Rpb25UeXBlOjI=',
            'answer': ['-', ],
        }

        cls.context = {
            'user': user,
        }

    def test_Should_IncludeDefiniteFieldsFromUserAnswerModel(self):
        expected_fields = [
            'attempt_id', 'question_id', 'answer',
        ]
        real_fields = list(self.tested_class().get_fields())

        self.assertEqual(expected_fields, real_fields)

    def test_When_EmptyData_Should_ErrorRequiredFields(self):
        data = {}

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_errors = {
            'attempt_id': [
                ErrorDetail(**{
                    'string': 'This field is required.',
                    'code': 'required',
                }),
            ],
            'question_id': [
                ErrorDetail(**{
                    'string': 'This field is required.',
                    'code': 'required',
                }),
            ],
            'answer': [
                ErrorDetail(**{
                    'string': 'This field is required.',
                    'code': 'required',
                }),
            ],
        }
        real_errors = _raise.exception.detail

        self.assertEqual(expected_errors, real_errors)

    def test_When_EmptyFields_Should_ErrorBlankFields(self):
        data = {
            'attempt_id': '',
            'question_id': '',
            'answer': [],
        }

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_errors = {
            'attempt_id': [
                ErrorDetail(**{
                    'string': 'This field may not be blank.',
                    'code': 'blank',
                }),
            ],
            'question_id': [
                ErrorDetail(**{
                    'string': 'This field may not be blank.',
                    'code': 'blank',
                }),
            ],
            'answer': [
                ErrorDetail(**{
                    'string': 'This list may not be empty.',
                    'code': 'empty',
                }),
            ],
        }
        real_errors = _raise.exception.detail

        self.assertEqual(expected_errors, real_errors)

    def test_When_AttemptIdIsNotBase64_Should_ErrorNotBase64(self):
        data = self.data_open_question
        data.update({
            'attempt_id': 'OjE=',
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_errors = {
            'attempt_id': [
                ErrorDetail(**{
                    'string': 'Not valid value.',
                    'code': 'invalid',
                }),
            ],
        }
        real_errors = _raise.exception.detail

        self.assertEqual(expected_errors, real_errors)

    def test_When_QuestionIdIsNotBase64_Should_ErrorNotBase64(self):
        data = self.data_open_question
        data.update({
            'question_id': 'OjE=',
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_errors = {
            'question_id': [
                ErrorDetail(**{
                    'string': 'Not valid value.',
                    'code': 'invalid',
                }),
            ],
        }
        real_errors = _raise.exception.detail

        self.assertEqual(expected_errors, real_errors)

    def test_When_CallValidateMethod_Should_ReturnValidatedData(self):
        data = self.data_open_question

        serializer = self.tested_class(data=data)
        serializer.is_valid()

        expected_validated_data = {
            'answer': [
                '-',
            ],
        }
        real_validated_data = serializer.validated_data

        self.assertEqual(expected_validated_data, real_validated_data)

    def test_When_AttemptIdNotFound_Should_ErrorNotFound(self):
        context = self.context
        data = self.data_open_question
        data.update({
            'attempt_id': 'VXNlckF0dGVtcHRUeXBlOjI=',
        })

        serializer = self.tested_class(data=data, context=context)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'attempt_id': [
                ErrorDetail(**{
                    'string': 'This attempt does not exist.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_QuestionIdNotFound_Should_ErrorNotFound(self):
        context = self.context
        data = self.data_open_question
        data.update({
            'question_id': 'UXVlc3Rpb25UeXBlOjM=',
        })

        serializer = self.tested_class(data=data, context=context)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'question_id': [
                ErrorDetail(**{
                    'string': 'This question does not exist.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_AttemptOtherUser_Should_ErrorNotHaveAccess(self):
        data = self.data_open_question
        context = self.context

        context.update({
            'user': self.user_without_access,
        })

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()

        with self.assertRaises(PermissionDenied) as _raise:
            serializer.save()

        expected_raise = {
            'attempt_id': [
                ErrorDetail(**{
                    'string': 'You do not have access to this attempt.',
                    'code': 'permission_denied',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_AttemptIsOver_Should_ErrorAttemptIsOver(self):
        user_attempt = self.user_attempt
        user_attempt.time_end = timezone.now() - timedelta(minutes=10)
        user_attempt.save()

        data = self.data_open_question
        context = self.context

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()

        with self.assertRaises(PermissionDenied) as _raise:
            serializer.save()

        expected_raise = {
            'attempt_id': [
                ErrorDetail(**{
                    'string': (
                        'The time for this attempt is over, the answers are '
                        'no longer counted.'
                    ),
                    'code': 'permission_denied',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_ManyAnswerOnOpenQuestion_Should_ErrorManyAnswers(self):
        data = self.data_open_question
        data.update({
            'answer': [
                '-',
                '-',
            ],
        })

        context = self.context

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'answer': [
                ErrorDetail(**{
                    'string': (
                        'For this question you cant give more than 1 answer.'
                    ),
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_AnswerOnOpenQuestionIsTrue_Should_SaveUserAnswerAsTrue(self):
        context = self.context
        data = self.data_open_question
        data.update({
            'answer': [
                'q' * 50,
            ],
        })

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()

        user_answer = serializer.save()
        real_is_true = user_answer.is_true

        self.assertTrue(real_is_true)

    def test_When_AnswerOnOpenQuestionIsFalse_Should_SaveUserAnswerAsFalse(
            self):
        context = self.context
        data = self.data_open_question
        data.update({
            'answer': [
                'q' * 49,
            ],
        })

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()

        user_answer = serializer.save()
        real_is_true = user_answer.is_true

        self.assertFalse(real_is_true)

    def test_When_AnswerOnChoiceQuestionIsTrue_Should_SaveUserAnswerAsTrue(
            self):
        data = self.data_choice_question
        data.update({
            'answer': [
                'QW5zd2VyVmFsdWVUeXBlOjI=',
            ],
        })

        context = self.context

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()

        user_answer = serializer.save()

        real_is_true = user_answer.is_true

        self.assertTrue(real_is_true)

    def test_When_AnswerOnChoiceQuestionIsFalse_Should_SaveUserAnswerAsFalse(
            self):
        data = self.data_choice_question
        data.update({
            'answer': [
                'QW5zd2VyVmFsdWVUeXBlOjI=', 'QW5zd2VyVmFsdWVUeXBlOjI=',
            ],
        })

        context = self.context

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()

        user_answer = serializer.save()

        real_is_true = user_answer.is_true

        self.assertFalse(real_is_true)

    def test_When_DuplicateAnswerOnQuestion_Should_ErrorDuplicateAnswer(self):
        data = self.data_open_question
        data.update({
            'answer': [
                'q' * 50,
            ],
        })

        context = self.context

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()
        serializer.save()

        serializer_duplicate = self.tested_class(data=data, context=context)
        serializer_duplicate.is_valid()

        with self.assertRaises(ValidationError) as _raise:
            serializer_duplicate.save()

        expected_raise = {
            'question_id': [
                ErrorDetail(**{
                    'string': (
                        'This question has already been answered in the '
                        'specified attempt.'
                    ),
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)
