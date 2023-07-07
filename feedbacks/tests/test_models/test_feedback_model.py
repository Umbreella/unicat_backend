from django.core.exceptions import ValidationError
from django.db.models import (BigAutoField, BooleanField, CharField,
                              DateTimeField, EmailField, TextField)
from django.test import TestCase
from django.utils import timezone

from ...models.Feedback import Feedback


class FeedbackModelTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Feedback

        cls.data = {
            'name': 'q' * 50,
            'email': 'q' * 50 + '@admin.com',
            'body': 'q' * 50,
        }

        cls.date_format = '%H-%M %d-%m-%Y'

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'id', 'name', 'email', 'body', 'created_at', 'is_closed',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'name': CharField,
            'email': EmailField,
            'body': TextField,
            'created_at': DateTimeField,
            'is_closed': BooleanField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'body': 'Message content.',
            'created_at': 'Date of writing the message.',
            'email': 'Email of the user who wrote.',
            'id': '',
            'is_closed': 'Has the message been processed.',
            'name': 'Full name of the user who wrote.',
        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_DataIsNone_Should_ErrorBlankField(self):
        category = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            category.save()

        expected_raise = {
            'name': [
                'This field cannot be blank.',
            ],
            'email': [
                'This field cannot be blank.',
            ],
            'body': [
                'This field cannot be blank.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataGreaterThanMaxLength_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'name': 'q' * 256,
            'email': 'q' * 119 + '@admin.com',
        })

        category = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            category.save()

        expected_raise = {
            'name': [
                'Ensure this value has at most 255 characters (it has 256).',
            ],
            'email': [
                'Ensure this value has at most 128 characters (it has 129).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SetDefaultValues(
            self):
        data = self.data

        feedback = self.tested_class(**data)
        feedback.save()

        expected_created_at = timezone.now().strftime(self.date_format)
        real_created_at = feedback.created_at.strftime(self.date_format)

        expected_is_closed = False
        real_is_closed = feedback.is_closed

        self.assertEqual(expected_created_at, real_created_at)
        self.assertEqual(expected_is_closed, real_is_closed)
