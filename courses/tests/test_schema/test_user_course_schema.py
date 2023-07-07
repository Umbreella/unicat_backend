import copy
from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.utils import timezone
from graphene import Context, Schema
from graphene.test import Client

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.LearningFormat import LearningFormat
from ...models.UserCourse import UserCourse
from ...schema.UserCourseType import UserCourseQuery


class UserCourseTypeTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = None

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

        first_course = Course.objects.create(**{
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
        })

        second_course = Course.objects.create(**{
            'id': 2,
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
        })

        third_course = Course.objects.create(**{
            'id': 3,
            'teacher': teacher,
            'title': 'w' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': first_category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        fourth_course = Course.objects.create(**{
            'id': 4,
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': second_category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        UserCourse.objects.create(**{
            'course': first_course,
            'user': first_user,
            'created_at': timezone.now(),
            'count_lectures_completed': 50,
            'count_independents_completed': 50,
        })

        UserCourse.objects.create(**{
            'course': second_course,
            'user': first_user,
            'created_at': timezone.now() - timedelta(minutes=10),
            'count_lectures_completed': 50,
            'count_independents_completed': 50,
        })

        UserCourse.objects.create(**{
            'course': third_course,
            'user': first_user,
        })

        UserCourse.objects.create(**{
            'course': fourth_course,
            'user': first_user,
        })

        context = Context()
        context.user = AnonymousUser()
        cls.context_with_anonymous_user = context

        context_with_user = copy.deepcopy(context)
        context_with_user.user = first_user
        cls.context_with_access = context_with_user

        contest_with_out_access = copy.deepcopy(context)
        contest_with_out_access.user = second_user
        cls.contest_with_out_access = contest_with_out_access

    def setUp(self):
        schema = Schema(query=UserCourseQuery)
        self.gql_client = Client(schema=schema)

    def test_When_SendQueryOnSingleCourseWithAnonser_Should_ErrorRequiredAuth(
            self):
        response = self.gql_client.execute(
            """
            query {
                myCourse (id: "Q291cnNlVHlwZTox") {
                    id
                }
            }
            """,
            context=self.context_with_anonymous_user,
        )

        expected_response = {
            'data': {
                'myCourse': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': ['myCourse', ],
                },
            ],
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithUserButWithOutAccess_Should_ErrorHaveNotAccess(
            self):
        response = self.gql_client.execute(
            """
            query {
                myCourse (id: "Q291cnNlVHlwZTox") {
                    id
                }
            }
            """,
            context=self.contest_with_out_access,
        )

        expected_response = {
            'data': {
                'myCourse': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'You don`t have access on this course.',
                    'path': ['myCourse', ],
                },
            ],
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithUserWithAccess_Should_ReturnData(self):
        response = self.gql_client.execute(
            """
            query {
                myCourse (id: "Q291cnNlVHlwZTox") {
                    id
                }
            }
            """,
            context=self.context_with_access,
        )

        expected_response = {
            'data': {
                'myCourse': {
                    'id': 'Q291cnNlVHlwZTox',
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithAnonymousUser_Should_ErrorRequiredAuth(self):
        response = self.gql_client.execute(
            """
            query {
                myCourses {
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
                'myCourses': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': ['myCourses', ],
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
                myCourses {
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
                'myCourses': {
                    'edges': [],
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithUserWithAccess_Should_ReturnCourseByUser(self):
        response = self.gql_client.execute(
            """
            query {
                myCourses {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
            context=self.context_with_access,
        )

        expected_response = {
            'data': {
                'myCourses': {
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

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithFilter_Should_ReturnFilteredData(self):
        response = self.gql_client.execute(
            """
            query GetFilteredMyCourse ($order_by: String, $search: String,
                                       $is_completed: Boolean, ) {
                myCourses (orderBy: $order_by, search: $search,
                            isCompleted: $is_completed,) {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
            variables={
                'order_by': 'created_at',
                'search': 'q',
                'is_completed': True,
            },
            context=self.context_with_access,
        )

        expected_response = {
            'data': {
                'myCourses': {
                    'edges': [
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
