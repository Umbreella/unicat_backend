import json
from datetime import timedelta

from django.conf import settings
from django.db import connections
from django.utils import timezone
from django.utils.connection import ConnectionProxy
from graphene import Context, Float, NonNull, Schema, String, relay
from graphene.test import Client
from graphene_django.utils import GraphQLTestCase
from rest_framework_simplejwt.tokens import RefreshToken

from unicat.graphql.loaders import Loaders
from users.models import User
from users.models.Teacher import Teacher
from users.schema.TeacherType import TeacherType

from ...models.Category import Category
from ...models.Course import Course
from ...models.CourseBody import CourseBody
from ...models.LearningFormat import LearningFormat
from ...models.UserCourse import UserCourse
from ...schema.CategoryType import CategoryType
from ...schema.CourseType import CourseQuery, CourseType
from ...schema.DiscountType import DiscountType


class CourseTypeTestCase(GraphQLTestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CourseType
        cls.model = Course

        cls.user = User.objects.create_superuser(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': cls.user,
            'description': 'q' * 50,
        })

        first_category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        second_category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        course = Course.objects.create(**{
            'id': 1,
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': first_category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
            'is_published': True,
        })

        Course.objects.create(**{
            'id': 2,
            'teacher': teacher,
            'title': 'w' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': second_category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        cls.course_body = CourseBody.objects.create(**{
            'course': course,
            'body': 'q' * 25,
        })

        UserCourse.objects.create(**{
            'course': course,
            'user': cls.user,
        })

        cls.discount_end_date = timezone.now() + timedelta(days=5)

        with ConnectionProxy(connections, 'master').cursor() as c:
            c.execute("""
            INSERT INTO courses_discount(
                percent,
                start_date,
                end_date,
                course_id
            )
            VALUES (5, '%s', '%s', 1);
            """ % (
                timezone.now() - timedelta(days=5),
                cls.discount_end_date,
            ))

        context = Context()
        context.build_absolute_uri = lambda x: 'build_absolute_uri'
        context.loaders = Loaders()
        cls.context = context

    def setUp(self):
        schema = Schema(query=CourseQuery)
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

    def test_Should_IncludeRequiredFieldsFromModel(self):
        expected_fields = [
            'id', 'teacher', 'category', 'title', 'price', 'count_lectures',
            'count_independents', 'count_listeners', 'duration', 'preview',
            'short_description', 'avg_rating', 'created_at', 'discount',
            'body', 'progress', 'learning_format',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'teacher': TeacherType,
            'category': CategoryType,
            'discount': DiscountType,
            'learning_format': String,
            'progress': Float,
            'body': String,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(field).__class__ == NonNull for field in [
                'id', 'created_at', 'count_independents', 'count_lectures',
                'count_listeners', 'duration', 'preview', 'price',
                'short_description', 'title', 'avg_rating',
            ]
        ])

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)

    def test_When_SendQueryWithHumanReadableLearningFormat_Should_ReturnData(
            self):
        response = self.query(
            """
            query GetCourse ($id: ID!) {
                course (id: $id) {
                    id
                    learningFormat
                }
            }
            """,
            variables={
                'id': 'Q291cnNlVHlwZTox',
            },
        )

        expected_response = {
            'data': {
                'course': {
                    'id': 'Q291cnNlVHlwZTox',
                    'learningFormat': 'Дистанционно',
                },
            },
        }
        real_response = json.loads(response.content)

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithAnonymousUser_Should_ReturnProgressIsNone(
            self):
        response = self.query(
            """
            query GetCourse ($id: ID!) {
                course (id: $id) {
                    id
                    progress
                }
            }
            """,
            variables={
                'id': 'Q291cnNlVHlwZTox',
            },
        )

        expected_response = {
            'data': {
                'course': {
                    'id': 'Q291cnNlVHlwZTox',
                    'progress': None,
                },
            },
            'errors': [
                {
                    'locations': [{'column': 21, 'line': 5}, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': ['course', 'progress', ],
                },
            ],
        }
        real_response = json.loads(response.content)

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithPreview_Should_ReturnFullUrlForFile(self):
        response = self.gql_client.execute(
            """
            query GetCourse ($id: ID!) {
                course (id: $id) {
                    preview
                }
            }
            """,
            variables={
                'id': 'Q291cnNlVHlwZTox',
            },
            context=self.context,
        )

        expected_url = {
            'data': {
                'course': {
                    'preview': 'build_absolute_uri',
                },
            },
        }
        real_url = response

        self.assertEqual(expected_url, real_url)

    def test_When_SendQueryListCourses_Should_ReturnListCourses(self):
        response = self.gql_client.execute(
            """
            query {
                allCourses {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
        )

        expected_response = {
            'data': {
                'allCourses': {
                    'edges': [
                        {
                            'node': {
                                'id': 'Q291cnNlVHlwZTox',
                            },
                        },
                    ],
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithFilters_Should_ReturnFilteredCourses(self):
        response = self.gql_client.execute(
            """
            query GetFilteredCourses ($orderBy: String, $search: String,
                                      $categoryId: String){
                allCourses (orderBy: $orderBy, search: $search,
                            categoryId: $categoryId, ) {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
            variables={
                'orderBy': '-created_at',
                'search': 'q',
                #   'Q2F0ZWdvcnlUeXBlOjE=' - 'CategoryType:1'
                'categoryId': 'Q2F0ZWdvcnlUeXBlOjE=',
            },
        )

        expected_response = {
            'data': {
                'allCourses': {
                    'edges': [
                        {
                            'node': {
                                'id': 'Q291cnNlVHlwZTox',
                            },
                        },
                    ],
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryListLatestCourses_Should_ReturnListLatestCourses(
            self):
        response = self.gql_client.execute(
            """
            query {
                latestCourses {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
        )

        expected_response = {
            'data': {
                'latestCourses': {
                    'edges': [
                        {
                            'node': {
                                'id': 'Q291cnNlVHlwZTox',
                            },
                        },
                    ],
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_CallRelatedData_Should_UseLoadersWithOutErrors(self):
        access_token = RefreshToken.for_user(self.user).access_token
        header = (
            f'{settings.SIMPLE_JWT.get("AUTH_HEADER_TYPES")[0]} {access_token}'
        )

        response = self.query(
            """
            query {
                allCourses {
                    edges {
                        node {
                            id
                            teacher {
                                id
                            }
                            category {
                                id
                            }
                            body
                            discount {
                                percent
                                endDate
                            }
                            progress
                        }
                    }
                }
            }
            """,
            headers={
                'HTTP_AUTHORIZATION': header,
            },
        )

        expected_response = {
            'data': {
                'allCourses': {
                    'edges': [
                        {
                            'node': {
                                'id': 'Q291cnNlVHlwZTox',
                                'teacher': {'id': 'VGVhY2hlclR5cGU6MQ==', },
                                'category': {'id': 'Q2F0ZWdvcnlUeXBlOjE=', },
                                'body': 'q' * 25,
                                'discount': {
                                    'percent': 5,
                                    'endDate': str(
                                        self.discount_end_date.date()
                                    ),
                                },
                                'progress': 0.0,
                            },
                        },
                    ],
                },
            },
        }
        real_response = json.loads(response.content)

        self.assertEqual(expected_response, real_response)
