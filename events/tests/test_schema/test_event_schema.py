import json
import tempfile

from django.conf import settings
from graphene_django.utils import GraphQLTestCase

from ...models.Event import Event


class EventTypeTestCase(GraphQLTestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        temporary_img = tempfile.NamedTemporaryFile(suffix=".jpg").name

        Event.objects.create(**{
            'preview': temporary_img,
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'date': '2001-01-01',
            'start_time': '12:00:00',
            'end_time': '12:00:00',
            'place': 'q' * 50,
        })

        cls.event_id = 'RXZlbnRUeXBlOjE='

    def test_When_SendQueryWithAllFields_Should_ReturnAllFields(self):
        response = self.query(
            '''
            query {
                event (id: "''' + self.event_id + '''") {
                    id
                    preview
                    title
                    shortDescription
                    description
                    date
                    startTime
                    endTime
                    place
                }
            }
            ''',
        )

        self.assertResponseNoErrors(response)

    def test_When_SendQueryWithPreview_Should_ReturnFullUrlForFile(self):
        response = self.query(
            '''
            query {
                event (id: "''' + self.event_id + '''") {
                    preview
                }
            }
            ''',
        )

        content = json.loads(response.content)

        expected_url = 'http://testserver' + settings.MEDIA_URL
        real_url = content['data']['event']['preview']

        self.assertIn(expected_url, real_url)

    def test_When_SendQueryListWithAllFields_Should_ReturnAllFields(self):
        response = self.query(
            '''
            query {
                allEvents {
                    edges {
                        node {
                            id
                            preview
                            title
                            shortDescription
                            description
                            date
                            startTime
                            endTime
                            place
                        }
                    }
                }
            }
            ''',
        )

        content = json.loads(response.content)

        expected_count_course = len(Event.objects.all())
        real_count_course = len(content['data']['allEvents']['edges'])

        self.assertResponseNoErrors(response)
        self.assertEqual(expected_count_course, real_count_course)
