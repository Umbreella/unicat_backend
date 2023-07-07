import json

from graphene import Int, List, NonNull, relay
from graphene_django.utils import GraphQLTestCase
from rest_framework_simplejwt.tokens import RefreshToken

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
from ...models.UserAttempt import UserAttempt
from ...models.UserLesson import UserLesson
from ...schema.QuestionType import QuestionType


class QuestionTypeTestCase(GraphQLTestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = QuestionType
        cls.model = Question

        cls.first_user = User.objects.create_superuser(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        cls.second_user = User.objects.create_superuser(**{
            'email': 'w' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': cls.first_user,
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
        })

        first_user_lesson = UserLesson.objects.create(**{
            'user': cls.first_user,
            'lesson': lesson,
        })

        UserAttempt.objects.create(**{
            'id': 1,
            'user_lesson': first_user_lesson,
        })

        UserAttempt.objects.create(**{
            'id': 2,
            'user_lesson': first_user_lesson,
        })

        question_open = Question.objects.create(**{
            'lesson': lesson,
            'body': 'question_open',
            'question_type': QuestionTypeChoices.FREE,
        })

        question_choice = Question.objects.create(**{
            'lesson': lesson,
            'body': 'question_choice',
            'question_type': QuestionTypeChoices.RADIOBUTTON,
        })

        Question.objects.create(**{
            'lesson': lesson,
            'body': 'question_with_out_answer',
            'question_type': QuestionTypeChoices.RADIOBUTTON,
        })

        AnswerValue.objects.create(**{
            'question': question_open,
            'value': 'q' * 50,
        })

        AnswerValue.objects.create(**{
            'question': question_choice,
            'value': 'answer_choice',
        })

    def test_Should_IncludeDefiniteDjangoModel(self):
        expected_model = self.model
        real_model = self.tested_class._meta.model

        self.assertEqual(expected_model, real_model)

    def test_Should_IncludeDefiniteInterfaces(self):
        expected_interfaces = [
            relay.Node,
        ]
        real_interfaces = list(self.tested_class._meta.interfaces)

        self.assertEqual(expected_interfaces, real_interfaces)

    def test_Should_IncludeAllFieldsFromModel(self):
        expected_fields = [
            'id', 'body', 'question_type', 'answers',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'question_type': Int,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(field).__class__ == NonNull for field in [
                'id', 'body',
            ]
        ])

        expected_answers = List
        real_answers = real_fields.pop('answers')

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)
        self.assertIsInstance(real_answers, expected_answers)

    def test_When_SendQueryWithNotAuthenticate_Should_ErrorHasNotPermission(
            self):
        response = self.query(
            """
            query {
                questions (attemptId: "UXVlc3Rpb25UeXBlOjE"){
                    id
                }
            }
            """,
        )

        expected_data = {
            'data': {
                'questions': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': ['questions', ],
                },
            ],
        }
        real_data = json.loads(response.content)

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithNotValidAttemptID_Should_ErrorNotValidAttemptID(
            self):
        access_token = RefreshToken.for_user(self.first_user).access_token
        response = self.query(
            """
            query {
                questions (attemptId: "UHJpdmF0ZUxlc3NvblR5cGU6MQ=="){
                    id
                }
            }
            """,
            headers={
                'HTTP_AUTHORIZATION': f'Bearer {access_token}',
            },
        )

        expected_data = {
            'data': {
                'questions': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'attemptId: not valid value.',
                    'path': ['questions', ],
                },
            ],
        }
        real_data = json.loads(response.content)

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithNotFoundAttemptID_Should_ErrorNotFoundAttemptID(
            self):
        access_token = RefreshToken.for_user(self.first_user).access_token
        response = self.query(
            """
            query {
                questions (attemptId: "VXNlckF0dGVtcHRUeXBlOjM="){
                    id
                }
            }
            """,
            headers={
                'HTTP_AUTHORIZATION': f'Bearer {access_token}',
            },
        )

        expected_data = {
            'data': {
                'questions': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'attemptId: not found value.',
                    'path': ['questions', ],
                },
            ],
        }
        real_data = json.loads(response.content)

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithNotAccess_Should_ErrorHasNotAccess(self):
        access_token = RefreshToken.for_user(self.second_user).access_token
        response = self.query(
            """
            query {
                questions (attemptId: "VXNlckF0dGVtcHRUeXBlOjI="){
                    id
                }
            }
            """,
            headers={
                'HTTP_AUTHORIZATION': f'Bearer {access_token}',
            },
        )

        expected_data = {
            'data': {
                'questions': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'You don`t have access on this attempt.',
                    'path': ['questions', ],
                },
            ],
        }
        real_data = json.loads(response.content)

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithValidAttemptID_Should_QuestionsInAttempt(
            self):
        access_token = RefreshToken.for_user(self.first_user).access_token
        response = self.query(
            """
            query {
                questions (attemptId: "VXNlckF0dGVtcHRUeXBlOjE="){
                    id
                    body
                    answers {
                        value
                    }
                }
            }
            """,
            headers={
                'HTTP_AUTHORIZATION': f'Bearer {access_token}',
            },
        )

        self.assertResponseNoErrors(response)
