import json

from graphene_django.utils import GraphQLTestCase

from ...models.Category import Category


class CategoryTypeTestCase(GraphQLTestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.first_category = Category.objects.create(**{
            'title': 'a' * 25,
        })

        cls.second_category = Category.objects.create(**{
            'title': 'c' * 25,
        })

        cls.third_category = Category.objects.create(**{
            'title': 'b' * 25,
        })

    def test_When_SendQueryListWithAllFields_Should_ReturnAllFields(self):
        response = self.query(
            '''
            query {
                allCategories {
                    edges {
                        node {
                            id
                            title
                        }
                    }
                }
            }
            ''',
        )

        self.assertResponseNoErrors(response)

    def test_When_SendQueryListWithOrderBy_Should_ReturnOrderedList(self):
        response = self.query(
            '''
            query {
                allCategories (orderBy: "title") {
                    edges {
                        node {
                            title
                        }
                    }
                }
            }
            ''',
        )

        content = json.loads(response.content)

        expected_nodes = [
            {'node': {'title': self.first_category.title}},
            {'node': {'title': self.third_category.title}},
            {'node': {'title': self.second_category.title}},
        ]
        real_nodes = content['data']['allCategories']['edges']

        self.assertEqual(expected_nodes, real_nodes)
