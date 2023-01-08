from django.test import TestCase
from graphene import Schema
from graphene.test import Client

from unicat.graphql.functions import get_value_from_model_id

from ...models.Category import Category
from ...schema.CategoryType import CategoryQuery, CategoryType


class CategoryTypeTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CategoryType

        cls.first_category = Category.objects.create(**{
            'title': 'a' * 25,
        })

        cls.second_category = Category.objects.create(**{
            'title': 'c' * 25,
        })

        cls.third_category = Category.objects.create(**{
            'title': 'b' * 25,
        })

    def setUp(self) -> None:
        schema = Schema(query=CategoryQuery)

        self.gql_client = Client(schema=schema)

    def test_Should_IncludeAllFieldsFromModel(self):
        expected_fields = [field.name for field in Category._meta.fields]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_When_SendQueryWithAllCategories_Should_ReturnWithOutErrors(self):
        response = self.gql_client.execute(
            '''
            query {
                allCategories {
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

        for category in Category.objects.values('id'):
            edges += [{
                'node': {
                    'id': get_value_from_model_id(model_name=model_name,
                                                  model_id=category['id'])
                }
            }]

        expected_data = {
            'data': {
                'allCategories': {
                    'edges': edges
                }
            }
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryListWithOrderBy_Should_ReturnOrderedList(self):
        response = self.gql_client.execute(
            '''
            query {
                allCategories (orderBy: "title") {
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

        for category in Category.objects.order_by('title').values('id'):
            edges += [{
                'node': {
                    'id': get_value_from_model_id(model_name=model_name,
                                                  model_id=category['id'])
                }
            }]

        expected_data = {
            'data': {
                'allCategories': {
                    'edges': edges
                }
            }
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
