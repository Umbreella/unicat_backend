import graphene
from django.test import TestCase
from graphene import Context, Schema
from graphene.test import Client

from ...models import User
from ...schema.UserType import UserType


class UserTypeTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserType

        cls.first_user = User.objects.create(**{
            'id': 1,
            'first_name': 'q' * 50,
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
            'photo': 'temporary_img',
        })

        cls.second_user = User.objects.create(**{
            'id': 2,
            'first_name': 'q' * 50,
            'email': 'w' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        context = Context()
        context.build_absolute_uri = lambda x: 'build_absolute_uri'
        cls.context = context

    def setUp(self) -> None:
        class TestQuery(graphene.ObjectType):
            users = graphene.List(self.tested_class)

            def resolve_users(self, *args, **kwargs):
                return User.objects.all()

        schema = Schema(query=TestQuery)
        self.gql_client = Client(schema=schema)

    def test_Should_IncludeFieldsFromModel(self):
        expected_fields = [
            'photo', 'name',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_When_SendQueryListTeachers_Should_ReturnListTeachers(self):
        response = self.gql_client.execute(
            """
            query {
                users {
                    photo
                    name
                }
            }
            """,
            context=self.context,
        )

        expected_response = {
            'data': {
                'users': [
                    {
                        'photo': 'build_absolute_uri',
                        'name': str(self.first_user),
                    },
                    {
                        'photo': None,
                        'name': str(self.second_user),
                    },
                ],
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)
