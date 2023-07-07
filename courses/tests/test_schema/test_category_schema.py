from django.test import TestCase
from graphene import NonNull, Schema, relay
from graphene.test import Client

from ...models.Category import Category
from ...schema.CategoryType import CategoryQuery, CategoryType


class CategoryTypeTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CategoryType
        cls.model = Category

        cls.first_category = Category.objects.create(**{
            'id': 1,
            'title': 'a' * 25,
        })

        cls.second_category = Category.objects.create(**{
            'id': 2,
            'title': 'c' * 25,
        })

        cls.third_category = Category.objects.create(**{
            'id': 3,
            'title': 'b' * 25,
        })

    def setUp(self):
        schema = Schema(query=CategoryQuery)
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
            'id', 'title',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': NonNull,
            'title': NonNull,
        }
        real_fields = {
            key: value.type.__class__
            for key, value in self.tested_class._meta.fields.items()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_When_SendQueryWithAllCategories_Should_ReturnWithOutErrors(self):
        response = self.gql_client.execute(
            """
            query {
                allCategories {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
        )

        expected_data = {
            'data': {
                'allCategories': {
                    'edges': [
                        {
                            'node': {
                                'id': 'Q2F0ZWdvcnlUeXBlOjE=',
                            },
                        },
                        {
                            'node': {
                                'id': 'Q2F0ZWdvcnlUeXBlOjI=',
                            },
                        },
                        {
                            'node': {
                                'id': 'Q2F0ZWdvcnlUeXBlOjM=',
                            },
                        },
                    ],
                },
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryListWithOrderBy_Should_ReturnOrderedList(self):
        response = self.gql_client.execute(
            """
            query {
                allCategories (orderBy: "title") {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
        )

        expected_data = {
            'data': {
                'allCategories': {
                    'edges': [
                        {
                            'node': {
                                'id': 'Q2F0ZWdvcnlUeXBlOjE=',
                            },
                        },
                        {
                            'node': {
                                'id': 'Q2F0ZWdvcnlUeXBlOjM=',
                            },
                        },
                        {
                            'node': {
                                'id': 'Q2F0ZWdvcnlUeXBlOjI=',
                            },
                        },
                    ],
                },
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
