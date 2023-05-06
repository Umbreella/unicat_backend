from django.test import TestCase
from graphene import NonNull, Schema
from graphene.test import Client

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.CourseStat import CourseStat
from ...models.LearningFormat import LearningFormat
from ...schema.CourseStatType import CourseStatQuery, CourseStatType


class CourseStatTypeTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CourseStatType
        cls.model = CourseStat

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

        Course.objects.create(**{
            'id': 1,
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

        Course.objects.create(**{
            'id': 2,
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

    def setUp(self):
        schema = Schema(query=CourseStatQuery)
        self.gql_client = Client(schema=schema)

    def test_Should_IncludeAllFieldsFromModel(self):
        expected_fields = (
            'id', 'avg_rating', 'count_comments', 'count_five_rating',
            'count_four_rating', 'count_three_rating', 'count_two_rating',
            'count_one_rating',
        )
        real_fields = tuple(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': NonNull,
            'avg_rating': NonNull,
            'count_comments': NonNull,
            'count_five_rating': NonNull,
            'count_four_rating': NonNull,
            'count_three_rating': NonNull,
            'count_two_rating': NonNull,
            'count_one_rating': NonNull,
        }
        real_fields = {
            key: value.type.__class__
            for key, value in self.tested_class._meta.fields.items()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_When_SendQueryWithNotValidCourseId_Should_ErrorNotValidValue(
            self):
        response = self.gql_client.execute(
            """
            query {
                statistic (courseId: "OjE=") {
                    id
                }
            }
            """,
        )

        expected_data = {
            'data': {
                'statistic': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3}],
                    'message': 'This is not global Id.',
                    'path': ['statistic'],
                },
            ],
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithNotFoundCourseId_Should_ReturnEmptyData(
            self):
        response = self.gql_client.execute(
            """
            query {
                statistic (courseId: "Q291cnNlVHlwZToz") {
                    id
                }
            }
            """,
        )

        expected_data = {
            'data': {
                'statistic': None,
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryListWithOrderBy_Should_ReturnOrderedList(self):
        response = self.gql_client.execute(
            """
            query {
                statistic (courseId: "Q291cnNlVHlwZTox") {
                    id
                }
            }
            """,
        )

        expected_data = {
            'data': {
                'statistic': {
                    'id': 'Q291cnNlU3RhdFR5cGU6MQ==',
                },
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
