from django.test import TestCase
from django.utils import timezone
from graphene import Schema
from graphene.test import Client

from unicat.graphql.functions import get_value_from_model_id
from users.models import User

from ...models.New import New
from ...schema.NewType import NewsQuery, NewType


class NewTypeTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = NewType

        cls.user = User.objects.create(**{
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        New.objects.bulk_create([
            New(**{
                'preview': 'temporary_img',
                'title': 'q' * 50,
                'short_description': 'q' * 50,
                'description': 'q' * 50,
                'author': cls.user,
            }),
            New(**{
                'preview': 'temporary_img',
                'title': 'q' * 50,
                'short_description': 'q' * 50,
                'description': 'q' * 50,
                'author': cls.user,
            }),
        ])

        cls.new_id = 'TmV3VHlwZTox'
        cls.date_format = "%d.%m.%Y"

    def setUp(self) -> None:
        schema = Schema(query=NewsQuery)

        self.gql_client = Client(schema=schema)

    def test_Should_IncludeAllFieldsFromModel(self):
        expected_fields = [field.name for field in New._meta.fields]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_When_SendQueryWithNewsId_Should_ReturnNewsByNewsId(self):
        response = self.gql_client.execute(
            '''
            query GetNews($newsId: ID!){
                news (id: $newsId) {
                    id
                    createdAt
                    author
                }
            }
            ''',
            variables={
                'newsId': self.new_id
            },
        )

        created_at = timezone.now().strftime(self.date_format)

        expected_response = {
            'data': {
                'news': {
                    'id': self.new_id,
                    'createdAt': created_at,
                    'author': str(self.user),
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithPreview_Should_ReturnFullUrlForFile(self):
        response = self.gql_client.execute(
            '''
            query GetNews($newsId: ID!){
                news (id: $newsId) {
                    preview
                }
            }
            ''',
            variables={
                'newsId': self.new_id
            },
        )

        expected_url = '\'NoneType\' object has no attribute ' \
                       '\'build_absolute_uri\''
        real_url = response['errors'][0]['message']

        self.assertEqual(expected_url, real_url)

    def test_When_SendQueryListNews_Should_ReturnListNews(self):
        response = self.gql_client.execute(
            '''
            query {
                allNews {
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

        for news in New.objects.order_by('-created_at').values('id'):
            edges += [{
                'node': {
                    'id': get_value_from_model_id(model_name=model_name,
                                                  model_id=news['id'])
                }
            }]

        expected_response = {
            'data': {
                'allNews': {
                    'edges': edges
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)
