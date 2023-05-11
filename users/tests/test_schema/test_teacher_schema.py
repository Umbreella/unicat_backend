from django.test import TestCase
from graphene import Context, Schema
from graphene.test import Client

from ...models import User
from ...models.Teacher import Teacher
from ...schema.TeacherType import TeacherQuery, TeacherType


class TeacherTypeTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = TeacherType

        user_with_photo = User.objects.create(**{
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
            'photo': 'temporary_img',
        })

        user_with_out_photo = User.objects.create(**{
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'w' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        Teacher.objects.create(**{
            'id': 1,
            'user': user_with_photo,
            'description': 'q' * 50,
            'average_rating': 1.0,
            'count_graduates': 1,
            'facebook': 'q' * 50,
            'twitter': 'q' * 50,
            'google_plus': 'q' * 50,
            'vk': 'q' * 50,
        })

        Teacher.objects.create(**{
            'id': 2,
            'user': user_with_out_photo,
            'description': 'q' * 50,
            'average_rating': 1.0,
            'count_graduates': 1,
            'facebook': 'q' * 50,
            'twitter': 'q' * 50,
            'google_plus': 'q' * 50,
            'vk': 'q' * 50,
        })

        context = Context()
        context.build_absolute_uri = lambda x: 'build_absolute_uri'
        cls.context = context

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
            """
            query {
                allTeachers {
                    edges {
                        node {
                            id
                            photo
                        }
                    }
                }
            }
            """,
            context=self.context,
        )

        expected_response = {
            'data': {
                'allTeachers': {
                    'edges': [
                        {
                            'node': {
                                'id': 'VGVhY2hlclR5cGU6MQ==',
                                'photo': 'build_absolute_uri',
                            }
                        },
                        {
                            'node': {
                                'id': 'VGVhY2hlclR5cGU6Mg==',
                                'photo': None,
                            }
                        },
                    ],
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithFullName_Should_ReturnFullNameForTeacher(self):
        response = self.gql_client.execute(
            """
            query {
                allTeachers (first: 1) {
                    edges {
                        node {
                            fullName
                        }
                    }
                }
            }
            """,
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
