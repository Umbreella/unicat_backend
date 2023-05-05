from django.core.exceptions import ValidationError
from django.db.models import (BigAutoField, CharField, DateField,
                              DateTimeField, ImageField, TextField, TimeField)
from django.test import TestCase

from ...models.Event import Event


class EventModelTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Event

        cls.data = {
            'preview': 'temporary_img',
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'date': '2001-01-01',
            'start_time': '12:00:00',
            'end_time': '12:00:00',
            'place': 'q' * 50,
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'id', 'preview', 'title', 'short_description', 'description',
            'date', 'start_time', 'end_time', 'place', 'created_at',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'preview': ImageField,
            'title': CharField,
            'short_description': CharField,
            'description': TextField,
            'date': DateField,
            'start_time': TimeField,
            'end_time': TimeField,
            'place': CharField,
            'created_at': DateTimeField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }
        self.maxDiff = None
        self.assertEqual(expected_fields, real_fields)

    def test_When_CreateCourseWithOutData_Should_ErrorBlankField(self):
        event = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            event.save()

        expected_raise = {
            'preview': [
                'This field cannot be blank.',
            ],
            'title': [
                'This field cannot be blank.',
            ],
            'short_description': [
                'This field cannot be blank.',
            ],
            'description': [
                'This field cannot be blank.',
            ],
            'date': [
                'This field cannot be null.',
            ],
            'start_time': [
                'This field cannot be null.',
            ],
            'end_time': [
                'This field cannot be null.',
            ],
            'place': [
                'This field cannot be blank.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataLengthGreaterThan255_Should_ErrorsMaxLength(self):
        data = self.data
        data.update({
            'title': 'q' * 275,
            'short_description': 'q' * 275,
            'place': 'q' * 275,
        })

        event = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            event.save()

        expected_raise = {
            'title': [
                'Ensure this value has at most 255 characters (it has 275).',
            ],
            'short_description': [
                'Ensure this value has at most 255 characters (it has 275).',
            ],
            'place': [
                'Ensure this value has at most 255 characters (it has 275).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SaveEventAndReturnTitleAsStr(self):
        data = self.data

        event = self.tested_class(**data)
        event.save()

        expected_str = event.title
        real_str = str(event)

        self.assertEqual(expected_str, real_str)
