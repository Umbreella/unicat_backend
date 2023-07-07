from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db.models import DateTimeField, ForeignKey, UUIDField
from django.test import TestCase
from django.utils import timezone

from ...models import User
from ...models.ResetPassword import ResetPassword


class UserModelTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = ResetPassword

        user = User.objects.create(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        cls.data = {
            'user': user,
        }

        cls.date_format = '%H-%M %d-%m-%Y'

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'user', 'url', 'closed_at',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'user': ForeignKey,
            'url': UUIDField,
            'closed_at': DateTimeField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'closed_at': 'Duration of the change request.',
            'url': 'A unique link to change your password.',
            'user': 'The user who requested a password change.',
        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreateResetPasswordWithOutData_Should_ErrorBlankField(self):
        reset_password = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            reset_password.save()

        expected_raise = {
            'user': [
                'This field cannot be null.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataIsValid_Should_CreateResetPassword(self):
        data = self.data

        reset_password = self.tested_class(**data)
        reset_password.save()

        after_ten_minutes = timezone.now() + timedelta(minutes=10)

        expected_closed_at = after_ten_minutes.strftime(self.date_format)
        real_raise = reset_password.closed_at.strftime(self.date_format)

        self.assertEqual(expected_closed_at, real_raise)
