import json

from django.utils import timezone
from graphene import NonNull, Schema, String, relay
from graphene.test import Client
from graphene_django.utils import GraphQLTestCase

from users.models import User

from ...models.New import New
from ...schema.NewType import NewsQuery, NewType


class NewTypeTestCase(GraphQLTestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = NewType
        cls.model = New

        cls.user = User.objects.create(**{
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        New.objects.create(**{
            'id': 1,
            'preview': 'temporary_img',
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'author': cls.user,
        })

        New.objects.create(**{
            'id': 2,
            'preview': 'temporary_img',
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'author': cls.user,
        })

        cls.new_id = 'TmV3VHlwZTox'
        cls.date_format = '%d.%m.%Y'

    def setUp(self):
        schema = Schema(query=NewsQuery)
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

    def test_Should_IncludeAllFieldsFromModel(self):
        expected_fields = [
            'id', 'preview', 'title', 'short_description', 'description',
            'author', 'created_at',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'created_at': String,
            'author': String,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(field).__class__ == NonNull for field in [
                'id', 'preview', 'title', 'short_description', 'description',
            ]
        ])

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)

    def test_When_SendQueryWithNewsId_Should_ReturnNewsByNewsId(self):
        response = self.gql_client.execute(
            """
            query GetNews($newsId: ID!){
                news (id: $newsId) {
                    id
                    createdAt
                }
            }
            """,
            variables={
                'newsId': self.new_id,
            },
        )

        created_at = timezone.now().strftime(self.date_format)

        expected_response = {
            'data': {
                'news': {
                    'id': self.new_id,
                    'createdAt': created_at,
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithPreview_Should_ReturnFullUrlForFile(self):
        response = self.gql_client.execute(
            """
            query GetNews($newsId: ID!){
                news (id: $newsId) {
                    preview
                }
            }
            """,
            variables={
                'newsId': self.new_id,
            },
        )

        expected_url = (
            "'NoneType' object has no attribute 'build_absolute_uri'"
        )
        real_url = response['errors'][0]['message']

        self.assertEqual(expected_url, real_url)

    def test_When_SendQueryListNews_Should_ReturnListNews(self):
        response = self.query(
            """
            query {
                allNews {
                    edges {
                        node {
                            id
                            author
                        }
                    }
                }
            }
            """,
        )

        expected_response = {
            'data': {
                'allNews': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TmV3VHlwZToy',
                                'author': str(self.user),
                            },
                        },
                        {
                            'node': {
                                'id': 'TmV3VHlwZTox',
                                'author': str(self.user),
                            },
                        },
                    ],
                },
            },
        }
        real_response = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertEqual(expected_response, real_response)
