from django.test import TestCase
from graphene import Schema
from graphene.test import Client

from unicat.graphql.functions import get_value_from_model_id

from ...models import User
from ...models.Teacher import Teacher
from ...schema.TeacherType import TeacherQuery, TeacherType


class TeacherTypeTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = TeacherType

        user = User.objects.create(**{
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
            'photo': 'temporary_img',
        })

        Teacher.objects.create(**{
            'user': user,
            'description': 'q' * 50,
            'average_rating': 1.0,
            'count_graduates': 1,
            'facebook': 'q' * 50,
            'twitter': 'q' * 50,
            'google_plus': 'q' * 50,
            'vk': 'q' * 50,
        })

    def setUp(self) -> None:
        schema = Schema(query=TeacherQuery)

        self.gql_client = Client(schema=schema)

    def test_Should_IncludeAllFieldsFromModel(self):
        expected_fields = [field.name for field in Teacher._meta.fields] + [
            'course_set', 'full_name', 'photo'
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_When_SendQueryListTeachers_Should_ReturnListTeachers(self):
        response = self.gql_client.execute(
            '''
            query {
                allTeachers {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            ''',
        )

        edges = []
        model_name = self.tested_class.__name__

        for teacher in Teacher.objects.values('id'):
            edges += [{
                'node': {
                    'id': get_value_from_model_id(model_name=model_name,
                                                  model_id=teacher['id'])
                }
            }]

        expected_response = {
            'data': {
                'allTeachers': {
                    'edges': edges
                }
            }
        }

        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithPhoto_Should_ReturnFullUrlForFile(self):
        response = self.gql_client.execute(
            '''
            query {
                allTeachers (first: 1) {
                    edges {
                        node {
                            photo
                        }
                    }
                }
            }
            ''',
        )

        expected_url = '\'NoneType\' object has no attribute ' \
                       '\'build_absolute_uri\''
        real_url = response['errors'][0]['message']

        self.assertEqual(expected_url, real_url)

    def test_When_SendQueryWithFullName_Should_ReturnFullNameForTeacher(self):
        response = self.gql_client.execute(
            '''
            query {
                allTeachers (first: 1) {
                    edges {
                        node {
                            fullName
                        }
                    }
                }
            }
            ''',
        )

        teacher = Teacher.objects.first()

        expected_response = {
            'data': {
                'allTeachers': {
                    'edges': [
                        {
                            'node': {
                                'fullName': teacher.user.get_fullname()
                            }
                        }
                    ]
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)
