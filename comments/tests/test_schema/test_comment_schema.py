from django.test import TestCase
from django.utils import timezone
from graphene import Schema
from graphene.test import Client

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from unicat.graphql.functions import get_value_from_model_id
from users.models import User
from users.models.Teacher import Teacher

from ...models.Comment import Comment
from ...models.CommentedType import CommentedType
from ...schema.CommentType import CommentQuery, CommentType


class CommentTypeTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CommentType

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
            'description': 'q' * 50,
        })

        cls.comment = Comment(**{
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedType.COURSE.value,
            'commented_id': 1,
            'rating': 5,
        })

        Comment.objects.bulk_create([
            cls.comment,
            Comment(**{
                'author': user,
                'body': 'q' * 50,
                'commented_type': CommentedType.NEWS.value,
                'commented_id': 1,
            }),
            Comment(**{
                'author': user,
                'body': 'q' * 50,
                'commented_type': CommentedType.EVENT.value,
                'commented_id': 1,
            })
        ])

        cls.date_format = "%d.%m.%Y"

    def setUp(self) -> None:
        schema = Schema(query=CommentQuery)

        self.gql_client = Client(schema=schema)

    def test_When_UseCommentType_Should_IncludeAllFieldsFromModel(self):
        expected_fields = [field.name for field in Comment._meta.get_fields()]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_When_SendQueryWithComments_Should_ReturnWithOutErrors(self):
        response = self.gql_client.execute(
            '''
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
            '''
        )

        model_name = self.tested_class.__name__

        comment = Comment.objects.first().__dict__
        edges = [{
            'node': {
                'id': get_value_from_model_id(model_name=model_name,
                                              model_id=comment['id'])
            }
        }]

        expected_response = {
            'data': {
                'allCourseComments': {
                    'edges': edges
                },
                'allEventComments': {
                    'edges': edges
                },
                'allNewsComments': {
                    'edges': edges
                },
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithCreatedAt_Should_ReturnFormattedData(self):
        response = self.gql_client.execute(
            '''
            query {
                allCourseComments (first: 1){
                    edges {
                        node {
                            createdAt
                        }
                    }
                }
            }
            ''',
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
            '''
            query {
                allCourseComments (courseId: "OjE="){
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            '''
        )

        edges = []
        model_name = self.tested_class.__name__

        comments = Comment.objects.all()
        filtered_comments = comments.filter(**{
            'commented_type': CommentedType.COURSE.value,
            'commented_id': 1
        })

        for comment in filtered_comments.values('id'):
            edges += [{
                'node': {
                    'id': get_value_from_model_id(model_name=model_name,
                                                  model_id=comment['id'])
                }
            }]

        expected_response = {
            'data': {
                'allCourseComments': {
                    'edges': edges
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SetNewsId_Should_ReturnNewsCommentsFilteredByNewsId(self):
        response = self.gql_client.execute(
            '''
            query {
                allNewsComments (newsId: "OjE="){
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            '''
        )

        edges = []
        model_name = self.tested_class.__name__

        comments = Comment.objects.all()
        filtered_comments = comments.filter(**{
            'commented_type': CommentedType.NEWS.value,
            'commented_id': 1
        })

        for comment in filtered_comments.values('id'):
            edges += [{
                'node': {
                    'id': get_value_from_model_id(model_name=model_name,
                                                  model_id=comment['id'])
                }
            }]

        expected_response = {
            'data': {
                'allNewsComments': {
                    'edges': edges
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SetEventId_Should_ReturnEventCommentsFilteredByEventId(self):
        response = self.gql_client.execute(
            '''
            query {
                allEventComments (eventId: "OjE="){
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            '''
        )

        edges = []
        model_name = self.tested_class.__name__

        comments = Comment.objects.all()
        filtered_comments = comments.filter(**{
            'commented_type': CommentedType.EVENT.value,
            'commented_id': 1
        })

        for comment in filtered_comments.values('id'):
            edges += [{
                'node': {
                    'id': get_value_from_model_id(model_name=model_name,
                                                  model_id=comment['id'])
                }
            }]

        expected_response = {
            'data': {
                'allEventComments': {
                    'edges': edges
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)
