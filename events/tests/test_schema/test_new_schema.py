import json
import tempfile

from django.conf import settings
from graphene_django.utils import GraphQLTestCase

from users.models import User

from ...models.New import New


class NewTypeTestCase(GraphQLTestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        temporary_img = tempfile.NamedTemporaryFile(suffix=".jpg").name

        cls.user = User.objects.create(**{
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        New.objects.create(**{
            'preview': temporary_img,
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'author': cls.user,
            'created_at': '2001-01-01'
        })

        cls.new_id = 'TmV3VHlwZTox'

    def test_When_SendQueryWithAllFields_Should_ReturnAllFields(self):
        response = self.query(
            '''
            query {
                new (id: "''' + self.new_id + '''") {
                    id
                    preview
                    title
                    shortDescription
                    description
                    author
                    createdAt
                }
            }
            ''',
        )

        self.assertResponseNoErrors(response)

    def test_When_SendQueryWithPreview_Should_ReturnFullUrlForFile(self):
        response = self.query(
            '''
            query {
                new (id: "''' + self.new_id + '''") {
                    preview
                }
            }
            ''',
        )

        content = json.loads(response.content)

        expected_url = 'http://testserver' + settings.MEDIA_URL
        real_url = content['data']['new']['preview']

        self.assertIn(expected_url, real_url)

    def test_When_SendQueryWithAuthor_Should_ReturnStrForUser(self):
        response = self.query(
            '''
            query {
                new (id: "''' + self.new_id + '''") {
                    author
                }
            }
            ''',
        )

        content = json.loads(response.content)

        expected_author = str(self.user)
        real_author = content['data']['new']['author']

        self.assertIn(expected_author, real_author)

    def test_When_SendQueryListWithAllFields_Should_ReturnAllFields(self):
        response = self.query(
            '''
            query {
                allNews {
                    edges {
                        node {
                            id
                            preview
                            title
                            shortDescription
                            description
                            author
                            createdAt
                        }
                    }
                }
            }
            ''',
        )

        content = json.loads(response.content)

        expected_count_course = len(New.objects.all())
        real_count_course = len(content['data']['allNews']['edges'])

        self.assertResponseNoErrors(response)
        self.assertEqual(expected_count_course, real_count_course)
