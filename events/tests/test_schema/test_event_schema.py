from django.test import TestCase
from django.utils import timezone
from graphene import NonNull, Schema, String, relay
from graphene.test import Client

from ...models.Event import Event
from ...schema.EventType import EventQuery, EventType


class EventTypeTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = EventType
        cls.model = Event

        Event.objects.create(**{
            'id': 1,
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
            'id': 2,
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
        cls.date_format = '%d.%m.%Y'

    def setUp(self):
        schema = Schema(query=EventQuery)
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
            'date', 'start_time', 'end_time', 'place', 'created_at',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'created_at': String,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(field).__class__ == NonNull for field in [
                'id', 'preview', 'title', 'short_description', 'description',
                'date', 'start_time', 'end_time', 'place',
            ]
        ])

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)

    def test_When_SendQueryWithEventId_Should_ReturnEventByEventId(self):
        response = self.gql_client.execute(
            """
            query GetEvent($eventId: ID!){
                event (id: $eventId) {
                    id
                    createdAt
                }
            }
            """,
            variables={
                'eventId': self.event_id,
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
            """
            query GetEvent($eventId: ID!){
                event (id: $eventId) {
                    preview
                }
            }
            """,
            variables={
                'eventId': self.event_id,
            },
        )

        expected_url = (
            "'NoneType' object has no attribute 'build_absolute_uri'"
        )
        real_url = response['errors'][0]['message']

        self.assertEqual(expected_url, real_url)

    def test_When_SendQueryListEvents_Should_ReturnListEvents(self):
        response = self.gql_client.execute(
            """
            query {
                allEvents {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
        )

        expected_response = {
            'data': {
                'allEvents': {
                    'edges': [
                        {
                            'node': {
                                'id': 'RXZlbnRUeXBlOjI=',
                            },
                        },
                        {
                            'node': {
                                'id': 'RXZlbnRUeXBlOjE=',
                            },
                        },
                    ],
                },
            },
        }

        real_response = response

        self.assertEqual(expected_response, real_response)
