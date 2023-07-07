import json

import graphene
from django.contrib.auth.models import AnonymousUser
from django.test import modify_settings
from django.urls import path
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from graphene import Boolean, Context, Schema
from graphene_django.utils import GraphQLTestCase
from graphene_django.views import GraphQLView
from graphql_sync_dataloaders import DeferredExecutionContext
from rest_framework.test import URLPatternsTestCase
from rest_framework_simplejwt.tokens import RefreshToken

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.UserLesson import UserLesson
from ...nodes.LessonTypeNode import LessonTypeNode
from ...schema.PrivateLessonType import PrivateLessonType
from ...schema.PublicLessonType import PublicLessonType


class PrivateLessonQuery(graphene.ObjectType):
    private_lesson = LessonTypeNode.Field(PrivateLessonType)


@modify_settings(
    MIDDLEWARE={
        'remove': 'users.middleware.CookiesMiddleware.CookiesMiddleware',
    }
)
class PrivateLessonTypeTestCase(GraphQLTestCase, URLPatternsTestCase):
    databases = {'master', }

    urlpatterns = [
        path(**{
            'route': 'graphql/',
            'view': csrf_exempt(GraphQLView.as_view(**{
                'schema': Schema(query=PrivateLessonQuery),
                'execution_context_class': DeferredExecutionContext,
            })),
            'name': 'graphql',
        }),
    ]

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = PrivateLessonType
        cls.base_class = PublicLessonType

        cls.user = User.objects.create_superuser(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': cls.user,
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
            'lesson_type': LessonTypeChoices.THEME,
        })

        Lesson.objects.create(**{
            'id': 2,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY,
            'parent': lesson,
        })

        Lesson.objects.create(**{
            'id': 3,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST,
            'parent': lesson,
        })

        UserLesson.objects.create(**{
            'lesson': lesson,
            'user': cls.user,
            'completed_at': timezone.now(),
        })

        context = Context()
        context.user = AnonymousUser()
        cls.context = context

    def test_Should_IncludeDefiniteDjangoModel(self):
        expected_model = self.base_class._meta.model
        real_model = self.tested_class._meta.model

        self.assertEqual(expected_model, real_model)

    def test_Should_IncludeDefiniteInterfaces(self):
        expected_interfaces = self.base_class._meta.interfaces
        real_interfaces = self.tested_class._meta.interfaces

        self.assertEqual(expected_interfaces, real_interfaces)

    def test_Should_IncludeDefiniteFieldsFromModel(self):
        expected_fields = [
            *list(self.base_class._meta.fields),
            'is_completed',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            **{
                key: value.type
                for key, value in self.base_class._meta.fields.items()
            },
            'is_completed': Boolean,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(f).__class__ == expected_fields.pop(f).__class__
            for f in [
                'id', 'title', 'description',
            ]
        ])

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)

    def test_When_SendQueryWithOutUser_Should_Errors(self):
        response = self.query(
            """
            query {
                privateLesson (id: "UHJpdmF0ZUxlc3NvblR5cGU6MQ==") {
                    isCompleted
                }
            }
            """,
        )

        expected_response = {
            'data': {
                'privateLesson': {
                    'isCompleted': None,
                },
            },
            'errors': [
                {
                    'locations': [{'column': 21, 'line': 4, }, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': ['privateLesson', 'isCompleted', ],
                },
            ],
        }
        real_response = json.loads(response.content)

        self.assertResponseHasErrors(response)
        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithParentId_Should_ReturnDataWithOutErrors(self):
        access_token = RefreshToken.for_user(self.user).access_token
        response = self.query(
            """
            query {
                privateLesson (id: "UHJpdmF0ZUxlc3NvblR5cGU6MQ==") {
                    id
                    title
                    description
                    lessonType
                    serialNumber
                    isCompleted
                }
            }
            """,
            headers={
                'HTTP_AUTHORIZATION': f'Bearer {access_token}',
            },
        )

        expected_response = {
            'data': {
                'privateLesson': {
                    'id': 'TGVzc29uVHlwZTox',
                    'title': 'q' * 50,
                    'description': 'q' * 50,
                    'lessonType': 'Тема',
                    'serialNumber': '1.',
                    'isCompleted': True,
                },
            },
        }
        real_response = json.loads(response.content)

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithChildrenId_Should_ReturnDataWithOutErrors(self):
        access_token = RefreshToken.for_user(self.user).access_token
        response = self.query(
            """
            query {
                privateLesson (id: "UHJpdmF0ZUxlc3NvblR5cGU6Mg==") {
                    id
                    title
                    description
                    lessonType
                    serialNumber
                    isCompleted
                }
            }
            """,
            headers={
                'HTTP_AUTHORIZATION': f'Bearer {access_token}',
            },
        )

        expected_response = {
            'data': {
                'privateLesson': {
                    'id': 'TGVzc29uVHlwZToy',
                    'title': 'q' * 50,
                    'description': 'q' * 50,
                    'lessonType': 'Теория',
                    'serialNumber': '1.1.',
                    'isCompleted': False,
                },
            },
        }
        real_response = json.loads(response.content)

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithTestId_Should_ReturnDataWithOutErrors(self):
        access_token = RefreshToken.for_user(self.user).access_token
        response = self.query(
            """
            query {
                privateLesson (id: "UHJpdmF0ZUxlc3NvblR5cGU6Mw==") {
                    id
                    title
                    description
                    lessonType
                    serialNumber
                    isCompleted
                }
            }
            """,
            headers={
                'HTTP_AUTHORIZATION': f'Bearer {access_token}',
            },
        )

        expected_response = {
            'data': {
                'privateLesson': {
                    'id': 'TGVzc29uVHlwZToz',
                    'title': 'q' * 50,
                    'description': 'q' * 50,
                    'lessonType': 'Тест',
                    'serialNumber': '1.1.',
                    'isCompleted': False,
                },
            },
        }
        real_response = json.loads(response.content)

        self.assertEqual(expected_response, real_response)
