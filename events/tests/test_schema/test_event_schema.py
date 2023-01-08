from django.test import TestCase
from django.utils import timezone
from graphene import Schema
from graphene.test import Client

from unicat.graphql.functions import get_value_from_model_id

from ...models.Event import Event
from ...schema.EventType import EventQuery, EventType


class EventTypeTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = EventType

        Event.objects.create(**{
            'preview': 'temporary_img',
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'date': '2001-01-01',
            'start_time': '12:00:00',
            'end_time': '12:00:00',
            'place': 'q' * 50,
        })

        Event.objects.create(**{
            'preview': 'temporary_img',
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'date': '2001-01-01',
            'start_time': '12:00:00',
            'end_time': '12:00:00',
            'place': 'q' * 50,
        })

        cls.event_id = 'RXZlbnRUeXBlOjE='
        cls.date_format = "%d.%m.%Y"

    def setUp(self) -> None:
        schema = Schema(query=EventQuery)

        self.gql_client = Client(schema=schema)

    def test_Should_IncludeAllFieldsFromModel(self):
        expected_fields = [field.name for field in Event._meta.fields]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_When_SendQueryWithEventId_Should_ReturnEventByEventId(self):
        response = self.gql_client.execute(
            '''
            query GetEvent($eventId: ID!){
                event (id: $eventId) {
                    id
                    createdAt
                }
            }
            ''',
            variables={
                'eventId': self.event_id
            },
        )

        created_at = timezone.now().strftime(self.date_format)

        expected_response = {
            'data': {
                'event': {
                    'id': self.event_id,
                    'createdAt': created_at
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithPreview_Should_ReturnFullUrlForFile(self):
        response = self.gql_client.execute(
            '''
            query GetEvent($eventId: ID!){
                event (id: $eventId) {
                    preview
                }
            }
            ''',
            variables={
                'eventId': self.event_id
            },
        )

        expected_url = '\'NoneType\' object has no attribute ' \
                       '\'build_absolute_uri\''
        real_url = response['errors'][0]['message']

        self.assertEqual(expected_url, real_url)

    def test_When_SendQueryListEvents_Should_ReturnListEvents(self):
        response = self.gql_client.execute(
            '''
            query {
                allEvents {
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

        for event in Event.objects.order_by('-created_at').values('id'):
            edges += [{
                'node': {
                    'id': get_value_from_model_id(model_name=model_name,
                                                  model_id=event['id'])
                }
            }]

        expected_response = {
            'data': {
                'allEvents': {
                    'edges': edges
                }
            }
        }

        real_response = response

        self.assertEqual(expected_response, real_response)
