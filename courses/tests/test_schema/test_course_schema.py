import copy
from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from django.db import connections
from django.test import TestCase
from django.utils import timezone
from django.utils.connection import ConnectionProxy
from graphene import Context, Float, NonNull, Schema, String
from graphene.test import Client

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.CourseBody import CourseBody
from ...models.LearningFormat import LearningFormat
from ...models.UserCourse import UserCourse
from ...schema.CourseType import CourseQuery, CourseType
from ...schema.DiscountType import DiscountType


class CourseTypeTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CourseType

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

        first_category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        second_category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        cls.course_title_q = 'q' * 50,
        cls.course_title_w = 'w' * 50,

        course_with_body = Course.objects.create(**{
            'id': 1,
            'teacher': teacher,
            'title': cls.course_title_q,
            'price': 50.0,
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': first_category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        course = Course.objects.create(**{
            'id': 2,
            'teacher': teacher,
            'title': cls.course_title_w,
            'price': 50.0,
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': first_category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        Course.objects.create(**{
            'id': 3,
            'teacher': teacher,
            'title': cls.course_title_q,
            'price': 500.0,
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': first_category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        Course.objects.create(**{
            'id': 4,
            'teacher': teacher,
            'title': cls.course_title_w,
            'price': 50.0,
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': second_category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        cls.course_body = CourseBody.objects.create(**{
            'course': course_with_body,
            'body': 'q' * 64,
        })

        UserCourse.objects.create(**{
            'course': course_with_body,
            'user': first_user,
        })

        UserCourse.objects.create(**{
            'course': course,
            'user': first_user,
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

        #   'Q291cnNlVHlwZTox' - 'CourseType:1'
        #   'Q291cnNlVHlwZToy' - 'CourseType:2'
        #   'Q291cnNlVHlwZToz' - 'CourseType:3'
        cls.course_id_with_access_and_body = 'Q291cnNlVHlwZTox'
        cls.course_id_with_access_and_with_out_body = 'Q291cnNlVHlwZToy'
        cls.course_id_with_out_access = 'Q291cnNlVHlwZToz'

        context = Context()
        context.build_absolute_uri = lambda x: 'build_absolute_uri'
        context.user = AnonymousUser()
        cls.context_with_anonymous_user = context

        context_copy = copy.deepcopy(context)
        context_copy.user = first_user
        cls.context_with_user_and_access = context_copy

        context_copy = copy.deepcopy(context)
        context_copy.user = second_user
        cls.context_with_user_but_without_access = context_copy

    def setUp(self):
        schema = Schema(query=CourseQuery)
        self.gql_client = Client(schema=schema)

    def test_Should_IncludeRequiredFieldsFromModel(self):
        expected_fields = [
            'id', 'teacher', 'title', 'price', 'count_lectures',
            'count_independents', 'duration', 'category', 'preview',
            'short_description', 'created_at', 'statistic', 'learning_format',
            'body', 'progress', 'discount',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'body': String,
            'discount': DiscountType,
            'learning_format': String,
            'progress': Float,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(field).__class__ == NonNull for field in [
                'id', 'created_at', 'count_independents', 'count_lectures',
                'duration', 'preview', 'price', 'short_description', 'title',
            ]
        ])

        all_fields_is_function = [
            callable(real_fields.pop(field)) for field in [
                'category', 'statistic', 'teacher',
            ]
        ]

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)
        self.assertTrue(all_fields_is_function)

    def test_When_SendQueryWithNotEmptyCourseBody_Should_ReturnCourseAndBody(
            self):
        response = self.gql_client.execute(
            """
            query GetCourse ($id: ID!) {
                course (id: $id) {
                    id
                    body
                    discount {
                        percent
                    }
                }
            }
            """,
            variables={
                'id': self.course_id_with_access_and_body,
            },
            context=self.context_with_user_and_access,
        )

        expected_response = {
            'data': {
                'course': {
                    'id': self.course_id_with_access_and_body,
                    'body': self.course_body.body,
                    'discount': {
                        'percent': 5,
                    },
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithEmptyCourseBody_Should_ReturnCourseAndEmptyBody(
            self):
        response = self.gql_client.execute(
            """
            query GetCourse ($id: ID!) {
                course (id: $id) {
                    id
                    body
                    discount {
                        percent
                    }
                }
            }
            """,
            variables={
                'id': self.course_id_with_access_and_with_out_body,
            },
            context=self.context_with_user_and_access,
        )

        expected_response = {
            'data': {
                'course': {
                    'id': self.course_id_with_access_and_with_out_body,
                    'body': None,
                    'discount': None,
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithHumanReadableLearningFormat_Should_ReturnData(
            self):
        response = self.gql_client.execute(
            """
            query GetCourse ($id: ID!) {
                course (id: $id) {
                    id
                    learningFormat
                }
            }
            """,
            variables={
                'id': self.course_id_with_out_access,
            },
            context=self.context_with_user_and_access,
        )

        expected_response = {
            'data': {
                'course': {
                    'id': self.course_id_with_out_access,
                    'learningFormat': 'Дистанционно',
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithAnonymousUser_Should_ReturnProgressIsNone(
            self):
        response = self.gql_client.execute(
            """
            query GetCourse ($id: ID!) {
                course (id: $id) {
                    id
                    progress
                }
            }
            """,
            variables={
                'id': self.course_id_with_access_and_body,
            },
            context=self.context_with_anonymous_user,
        )

        expected_response = {
            'data': {
                'course': {
                    'id': self.course_id_with_access_and_body,
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
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithUserButWithOutAccess_Should_ReturnProgress(
            self):
        response = self.gql_client.execute(
            """
            query GetCourse ($id: ID!) {
                course (id: $id) {
                    id
                    progress
                }
            }
            """,
            variables={
                'id': self.course_id_with_access_and_body,
            },
            context=self.context_with_user_but_without_access,
        )

        expected_response = {
            'data': {
                'course': {
                    'id': self.course_id_with_access_and_body,
                    'progress': None,
                },
            },
            'errors': [
                {
                    'locations': [{'column': 21, 'line': 5, }, ],
                    'message': 'You don`t have access on this course.',
                    'path': ['course', 'progress', ],
                },
            ],
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithUserAndAccess_Should_ReturnProgress(self):
        response = self.gql_client.execute(
            """
            query GetCourse ($id: ID!) {
                course (id: $id) {
                    id
                    progress
                }
            }
            """,
            variables={
                'id': self.course_id_with_access_and_body,
            },
            context=self.context_with_user_and_access,
        )

        expected_response = {
            'data': {
                'course': {
                    'id': self.course_id_with_access_and_body,
                    'progress': 0.0,
                },
            },
        }
        real_response = response

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
                'id': self.course_id_with_access_and_body,
            },
            context=self.context_with_user_and_access,
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
                        {
                            'node': {
                                'id': 'Q291cnNlVHlwZToy',
                            },
                        },
                        {
                            'node': {
                                'id': 'Q291cnNlVHlwZToz',
                            },
                        },
                        {
                            'node': {
                                'id': 'Q291cnNlVHlwZTo0',
                            },
                        },
                    ],
                },
            },
        }
        real_response = response

        self.maxDiff = None

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
                                'id': 'Q291cnNlVHlwZToz',
                            },
                        },
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
                                'id': 'Q291cnNlVHlwZTo0',
                            },
                        },
                        {
                            'node': {
                                'id': 'Q291cnNlVHlwZToz',
                            },
                        },
                        {
                            'node': {
                                'id': 'Q291cnNlVHlwZToy',
                            },
                        },
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
