from django.test import TestCase
from django.utils import timezone
from graphene import Int, NonNull, Schema, String
from graphene.test import Client

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from events.models.Event import Event
from events.models.New import New
from unicat.graphql.functions import get_value_from_model_id
from users.models import User
from users.models.Teacher import Teacher
from users.schema.UserType import UserType

from ...models.Comment import Comment
from ...models.CommentedTypeChoices import CommentedTypeChoices
from ...schema.CommentType import CommentQuery, CommentType


class CommentTypeTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CommentType
        cls.model = Comment

        user = User.objects.create(**{
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

        Event.objects.create(**{
            'id': 1,
            'preview': 'temporary_img',
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'date': '2001-01-01',
            'start_time': '12:00:00',
            'end_time': '12:00:00',
            'place': 'q' * 50,
        })

        New.objects.create(**{
            'preview': 'temporary_img',
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'author': user,
        })

        cls.comment = Comment.objects.create(**{
            'id': 1,
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedTypeChoices.COURSE.value,
            'commented_id': 1,
            'rating': 5,
        })

        Comment.objects.create(**{
            'id': 2,
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedTypeChoices.NEWS.value,
            'commented_id': 1,
        })

        Comment.objects.create(**{
            'id': 3,
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedTypeChoices.EVENT.value,
            'commented_id': 1,
        })

        cls.date_format = '%d.%m.%Y'

    def setUp(self):
        schema = Schema(query=CommentQuery)
        self.gql_client = Client(schema=schema)

    def test_When_UseCommentType_Should_IncludeAllFieldsFromModel(self):
        expected_fields = [
            field.name for field in self.model._meta.fields
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'author': UserType,
            'created_at': String,
            'rating': Int,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(field).__class__ == NonNull for field in [
                'id', 'body', 'count_like', 'commented_type', 'commented_id',
            ]
        ])

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)

    def test_When_SendQueryWithComments_Should_ReturnWithOutErrors(self):
        response = self.gql_client.execute(
            """
            query {
                allCourseComments (first: 1){
                    edges {
                        node {
                            id
                        }
                    }
                }
                allNewsComments (first: 1){
                    edges {
                        node {
                            id
                        }
                    }
                }
                allEventComments (first: 1){
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """
        )

        expected_response = {
            'data': {
                'allCourseComments': {
                    'edges': [
                        {
                            'node': {
                                'id': 'Q29tbWVudFR5cGU6MQ==',
                            },
                        },
                    ],
                },
                'allEventComments': {
                    'edges': [
                        {
                            'node': {
                                'id': 'Q29tbWVudFR5cGU6MQ==',
                            },
                        },
                    ],
                },
                'allNewsComments': {
                    'edges': [
                        {
                            'node': {
                                'id': 'Q29tbWVudFR5cGU6MQ==',
                            },
                        },
                    ],
                },
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithCreatedAt_Should_ReturnFormattedData(self):
        response = self.gql_client.execute(
            """
            query {
                allCourseComments (first: 1){
                    edges {
                        node {
                            createdAt
                        }
                    }
                }
            }
            """,
        )

        created_at = timezone.now().strftime(self.date_format)

        expected_response = {
            'data': {
                'allCourseComments': {
                    'edges': [{'node': {'createdAt': created_at}}]
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SetCourseId_Should_ReturnCourseCommentsFilteredByCourseId(
            self):
        response = self.gql_client.execute(
            """
            query {
                allCourseComments (courseId: "Q291cnNlVHlwZTox"){
                    totalCount
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """
        )

        edges = []
        model_name = self.tested_class.__name__
        filtered_comments = Comment.objects.filter(**{
            'commented_type': CommentedTypeChoices.COURSE.value,
            'commented_id': 1
        }).values('id')

        for comment in filtered_comments:
            edges += [{
                'node': {
                    'id': get_value_from_model_id(model_name=model_name,
                                                  model_id=comment['id'])
                }
            }]

        expected_response = {
            'data': {
                'allCourseComments': {
                    'totalCount': 1,
                    'edges': edges
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SetNewsId_Should_ReturnNewsCommentsFilteredByNewsId(self):
        response = self.gql_client.execute(
            """
            query {
                allNewsComments (newsId: "TmV3VHlwZTox"){
                    totalCount
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """
        )

        edges = []
        model_name = self.tested_class.__name__
        filtered_comments = Comment.objects.filter(**{
            'commented_type': CommentedTypeChoices.NEWS.value,
            'commented_id': 1
        }).values('id')

        for comment in filtered_comments:
            edges += [{
                'node': {
                    'id': get_value_from_model_id(model_name=model_name,
                                                  model_id=comment['id'])
                }
            }]

        expected_response = {
            'data': {
                'allNewsComments': {
                    'totalCount': 1,
                    'edges': edges
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SetEventId_Should_ReturnEventCommentsFilteredByEventId(self):
        response = self.gql_client.execute(
            """
            query {
                allEventComments (eventId: "RXZlbnRUeXBlOjE="){
                    totalCount
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """
        )

        edges = []
        model_name = self.tested_class.__name__
        filtered_comments = Comment.objects.filter(**{
            'commented_type': CommentedTypeChoices.EVENT.value,
            'commented_id': 1
        }).values('id')

        for comment in filtered_comments:
            edges += [{
                'node': {
                    'id': get_value_from_model_id(model_name=model_name,
                                                  model_id=comment['id'])
                }
            }]

        expected_response = {
            'data': {
                'allEventComments': {
                    'totalCount': 1,
                    'edges': edges
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)
