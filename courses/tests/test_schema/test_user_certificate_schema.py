import copy

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.utils import timezone
from graphene import Context, NonNull, Schema, String
from graphene.test import Client

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.LearningFormat import LearningFormat
from ...models.UserCourse import UserCourse
from ...schema.UserCertificateType import (UserCertificateQuery,
                                           UserCertificateType)


class UserCertificateTypeTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserCertificateType

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

        UserCourse.objects.create(**{
            'course': cls.course,
            'user': first_user,
            'completed_at': timezone.now(),
        })

        context = Context()
        context.user = AnonymousUser()
        context.build_absolute_uri = lambda x: 'build_absolute_uri'
        cls.context_with_anonymous_user = context

        context_with_user = copy.deepcopy(context)
        context_with_user.user = first_user
        cls.context_with_access = context_with_user

        contest_with_out_access = copy.deepcopy(context)
        contest_with_out_access.user = second_user
        cls.contest_with_out_access = contest_with_out_access

        cls.date_format = '%d.%m.%Y'

    def setUp(self):
        schema = Schema(query=UserCertificateQuery)
        self.gql_client = Client(schema=schema)

    def test_Should_IncludeDefiniteFieldsFromModel(self):
        expected_fields = [
            'id', 'course', 'title', 'created_at',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'course': String,
            'title': String,
            'created_at': String,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        expected_id_class = NonNull
        real_id_class = real_fields.pop('id').__class__

        self.assertEqual(expected_fields, real_fields)
        self.assertEqual(expected_id_class, real_id_class)

    def test_When_SendQueryWithAnonymousUser_Should_ErrorHaveNotAccess(
            self):
        response = self.gql_client.execute(
            """
            query {
                myCertificates {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
            context=self.context_with_anonymous_user,
        )

        expected_response = {
            'data': {
                'myCertificates': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': ['myCertificates', ],
                },
            ],
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithUserButWithOutAccess_Should_ReturnEmptyData(
            self):
        response = self.gql_client.execute(
            """
            query {
                myCertificates {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
            context=self.contest_with_out_access,
        )

        expected_response = {
            'data': {
                'myCertificates': {
                    'edges': [],
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithUserWithAccess_Should_ReturnCertificatesByUser(
            self):
        response = self.gql_client.execute(
            """
            query {
                myCertificates {
                    edges {
                        node {
                            id
                            course
                            title
                            createdAt
                        }
                    }
                }
            }
            """,
            context=self.context_with_access,
        )

        timezone_now = timezone.now()
        created_at = timezone_now.strftime(self.date_format)

        expected_response = {
            'data': {
                'myCertificates': {
                    'edges': [
                        {
                            'node': {
                                'id': 'VXNlckNlcnRpZmljYXRlVHlwZTox',
                                'course': 'Q291cnNlVHlwZTox',
                                'title': str(self.course),
                                'createdAt': created_at,
                            },
                        },
                    ],
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)
