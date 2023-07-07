from datetime import timedelta

from django.db import connections
from django.utils import timezone
from django.utils.connection import ConnectionProxy
from graphene import Context, DateTime, Int, NonNull, Schema, relay
from graphene.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from courses.models.UserCourse import UserCourse
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.UserAttempt import UserAttempt
from ...models.UserLesson import UserLesson
from ...schema.UserAttemptType import UserAttemptQuery, UserAttemptType


class UserAttemptTypeTestCase(JSONWebTokenTestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserAttemptType
        cls.model = UserAttempt

        first_user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        second_user = User.objects.create_user(**{
            'email': 'w' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': first_user,
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
            'id': 1,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST,
        })

        Lesson.objects.create(**{
            'id': 2,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME,
        })

        Lesson.objects.create(**{
            'id': 3,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY,
        })

        UserCourse.objects.create(**{
            'course': course,
            'user': first_user,
        })

        UserLesson.objects.create(**{
            'id': 1,
            'lesson': lesson,
            'user': first_user,
        })

        with ConnectionProxy(connections, 'master').cursor() as c:
            c.execute("""
            INSERT INTO lessons_userattempt(
                time_start,
                time_end,
                count_true_answer,
                user_lesson_id
            )
            VALUES ('%s', '%s', 0, 1);
            """ % (
                timezone.now() - timedelta(days=2),
                timezone.now() - timedelta(days=1),
            ))
            c.execute("""
            INSERT INTO lessons_userattempt(
                time_start,
                time_end,
                count_true_answer,
                user_lesson_id
            )
            VALUES ('%s', '%s', 0, 1);
            """ % (
                timezone.now() - timedelta(days=1),
                timezone.now() + timedelta(days=1),
            ))

        context_with_access = Context()
        context_with_access.user = first_user
        cls.context_with_access = context_with_access

        context_with_out_access = Context()
        context_with_out_access.user = second_user
        cls.context_with_out_access = context_with_out_access

    def setUp(self):
        schema = Schema(query=UserAttemptQuery)
        self.gql_client = Client(schema=schema)

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

    def test_Should_IncludeDefiniteFieldsFromModel(self):
        expected_fields = [
            'id', 'time_end', 'count_true_answer', 'duration',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'time_end': DateTime,
            'duration': Int,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(field).__class__ == NonNull for field in [
                'id', 'count_true_answer',
            ]
        ])

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)

    def test_When_SendQueryWithNotAuthenticate_Should_ErrorHasNotPermission(
            self):
        response = self.client.execute(
            """
            query GetAttemptsByLesson ($lessonId: String!){
                myAttempts (lessonId: $lessonId){
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
            variables={
                'lessonId': 'TGVzc29uVHlwZTox',
            },
        )

        expected_data = {
            'data': {
                'myAttempts': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': ['myAttempts', ],
                },
            ],
        }
        real_data = response.formatted

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithNotValidLessonID_Should_ErrorNotValidLessonID(
            self):
        response = self.gql_client.execute(
            """
            query GetAttemptsByLesson ($lessonId: String!){
                myAttempts (lessonId: $lessonId){
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
            variables={
                'lessonId': 'OjE=',
            },
            context=self.context_with_access,
        )

        expected_data = {
            'data': {
                'myAttempts': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'lessonId: not valid value.',
                    'path': ['myAttempts', ],
                },
            ],
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithLessonIDNotFound_Should_ErrorLessonIDNotFound(
            self):
        response = self.gql_client.execute(
            """
            query GetAttemptsByLesson ($lessonId: String!){
                myAttempts (lessonId: $lessonId){
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
            variables={
                'lessonId': 'TGVzc29uVHlwZTo1',
            },
            context=self.context_with_access,
        )

        expected_data = {
            'data': {
                'myAttempts': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'Lesson with this id is not found.',
                    'path': ['myAttempts', ],
                },
            ],
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithNotAccessOnCourse_Should_ErrorHasNotAccess(
            self):
        response = self.gql_client.execute(
            """
            query GetAttemptsByLesson ($lessonId: String!){
                myAttempts (lessonId: $lessonId){
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
            variables={
                'lessonId': 'TGVzc29uVHlwZTox',
            },
            context=self.context_with_out_access,
        )

        expected_data = {
            'data': {
                'myAttempts': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'You do not have access to this lesson.',
                    'path': ['myAttempts', ],
                },
            ],
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithLessonTypeTheme_Should_ErrorNotValidLessonType(
            self):
        response = self.gql_client.execute(
            """
            query GetAttemptsByLesson ($lessonId: String!){
                myAttempts (lessonId: $lessonId){
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
            variables={
                'lessonId': 'TGVzc29uVHlwZToy',
            },
            context=self.context_with_access,
        )

        expected_data = {
            'data': {
                'myAttempts': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'Lesson this type has no attempts.',
                    'path': ['myAttempts', ],
                },
            ],
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithLessonTypeTheory_Should_ErrorNotValidLessonType(
            self):
        response = self.gql_client.execute(
            """
            query GetAttemptsByLesson ($lessonId: String!){
                myAttempts (lessonId: $lessonId){
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
            variables={
                'lessonId': 'TGVzc29uVHlwZToz',
            },
            context=self.context_with_access,
        )

        expected_data = {
            'data': {
                'myAttempts': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'Lesson this type has no attempts.',
                    'path': ['myAttempts', ],
                },
            ],
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithValidLessonID_Should_ReturnDataWithOutErrors(
            self):
        response = self.gql_client.execute(
            """
            query GetAttemptsByLesson ($lessonId: String!){
                myAttempts (lessonId: $lessonId){
                    edges {
                        node {
                            id
                            duration
                        }
                    }
                }
            }
            """,
            variables={
                'lessonId': 'TGVzc29uVHlwZTox',
            },
            context=self.context_with_access,
        )

        expected_data = {
            'data': {
                'myAttempts': {
                    'edges': [
                        {
                            'node': {
                                'id': 'VXNlckF0dGVtcHRUeXBlOjE=',
                                'duration': 86400,
                            },
                        },
                    ],
                },
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
