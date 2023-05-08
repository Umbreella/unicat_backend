from django.utils import timezone
from graphene import Boolean, Context, Float, NonNull, Schema, String, relay
from graphene.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from courses.models.UserCourse import UserCourse
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonBody import LessonBody
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.UserLesson import UserLesson
from ...schema.LessonType import LessonQuery, LessonType


class LessonTypeTestCase(JSONWebTokenTestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LessonType
        cls.model = Lesson

        user_with_access = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        user_without_access = User.objects.create_user(**{
            'email': 'w' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': user_with_access,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        course_with_access = Course.objects.create(**{
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

        course_with_out_access = Course.objects.create(**{
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

        lesson_with_body_complete = Lesson.objects.create(**{
            'id': 1,
            'course': course_with_access,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME,
        })

        Lesson.objects.create(**{
            'id': 2,
            'course': course_with_access,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME,
        })

        Lesson.objects.create(**{
            'id': 3,
            'course': course_with_out_access,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME,
        })

        UserLesson.objects.create(**{
            'lesson': lesson_with_body_complete,
            'user': user_with_access,
            'completed_at': timezone.now(),
        })

        cls.lesson_body = LessonBody.objects.create(**{
            'lesson': lesson_with_body_complete,
            'body': 'q' * 50,
        })

        UserCourse.objects.create(**{
            'course': course_with_access,
            'user': user_with_access,
        })

        #   'TGVzc29uVHlwZTox' - 'LessonType:1'
        #   'TGVzc29uVHlwZToy' - 'LessonType:2'
        #   'TGVzc29uVHlwZToz' - 'LessonType:3'
        cls.lesson_id_with_access = 'TGVzc29uVHlwZTox'
        cls.lesson_id_with_access_and_with_out_body = 'TGVzc29uVHlwZToy'
        cls.lesson_id_with_out_access = 'TGVzc29uVHlwZToz'

        context_with_access = Context()
        context_with_access.user = user_with_access
        cls.context_with_access = context_with_access

        context_without_access = Context()
        context_without_access.user = user_without_access
        cls.context_without_access = context_without_access

    def setUp(self):
        schema = Schema(query=LessonQuery)
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
            'id', 'serial_number', 'title', 'description', 'lesson_type',
            'time_limit', 'count_questions', 'body', 'is_completed',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'body': String,
            'lesson_type': String,
            'serial_number': String,
            'is_completed': Boolean,
            'time_limit': Float,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(field).__class__ == NonNull for field in [
                'id', 'title', 'description', 'count_questions',
            ]
        ])

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)

    def test_When_SendQueryWithOutAuthenticate_Should_ErrorHasNotPermission(
            self):
        response = self.client.execute(
            """
            query GetLesson ($id: ID!) {
                lesson (id: $id) {
                    id
                }
            }
            """,
            variables={
                'id': self.lesson_id_with_out_access,
            },
        )

        expected_response = {
            'data': {
                'lesson': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': ['lesson', ],
                },
            ],
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithOutAccess_Should_ErrorNotHaveAccess(self):
        response = self.gql_client.execute(
            """
            query GetLesson ($id: ID!) {
                lesson (id: $id) {
                    id
                    body
                }
            }
            """,
            variables={
                'id': self.lesson_id_with_out_access,
            },
            context=self.context_without_access,
        )

        expected_response = {
            'data': {
                'lesson': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'You do not have access to this lesson.',
                    'path': ['lesson', ],
                },
            ],
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithAccess_Should_ReturnLessonAndLessonBody(self):
        response = self.gql_client.execute(
            """
            query GetLesson ($id: ID!) {
                lesson (id: $id) {
                    id
                    body
                    lessonType
                    isCompleted
                }
            }
            """,
            variables={
                'id': self.lesson_id_with_access,
            },
            context=self.context_with_access,
        )

        expected_response = {
            'data': {
                'lesson': {
                    'id': self.lesson_id_with_access,
                    'body': self.lesson_body.body,
                    'lessonType': 'Тема',
                    'isCompleted': True,
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryLessonWithOutLessonBody_Should_ReturnLessonAndNull(
            self):
        response = self.gql_client.execute(
            """
            query GetLesson ($id: ID!) {
                lesson (id: $id) {
                    id
                    body
                    isCompleted
                }
            }
            """,
            variables={
                'id': self.lesson_id_with_access_and_with_out_body,
            },
            context=self.context_with_access,
        )

        expected_response = {
            'data': {
                'lesson': {
                    'id': self.lesson_id_with_access_and_with_out_body,
                    'body': None,
                    'isCompleted': False,
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)
