from django.core.exceptions import ValidationError
from django.db.models import DateTimeField, EmailField, ForeignKey, UUIDField
from django.test import TestCase

from ...models import User
from ...models.ChangeEmail import ChangeEmail


class UserModelTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = ChangeEmail

        cls.user = User.objects.create(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        User.objects.create(**{
            'email': 'w' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        cls.data = {
            'user': cls.user,
            'email': 'e' * 50 + '@q.qq',
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'user', 'url', 'prev_email', 'email', 'closed_at',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'user': ForeignKey,
            'url': UUIDField,
            'email': EmailField,
            'prev_email': EmailField,
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
            'email': 'New user email.',
            'prev_email': 'Current user email.',
            'url': 'A unique link to confirm the shift.',
            'user': 'The user who requested the email change.',
        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreateChangeEmailWithOutData_Should_ErrorBlankField(self):
        change_email = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            change_email.save()

        expected_raise = {
            'email': [
                'This field cannot be blank.',
            ],
            'user': [
                'This field cannot be null.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_LengthDataGreaterThan128_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'email': 'q' * 125 + '@q.qq',
        })

        user = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            user.save()

        expected_raise = {
            'email': [
                'Ensure this value has at most 128 characters (it has 130).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_PrevEmailIsNewEmail_Should_ErrorCantChangeEmail(self):
        data = self.data
        data.update({
            'email': 'q' * 50 + '@q.qq',
        })

        change_email = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            change_email.save()

        expected_raise = {
            'email': [
                'You cannot use this email as a new email.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_NewEmailIsUsed_Should_ErrorCantChangeEmail(self):
        data = self.data
        data.update({
            'email': 'w' * 50 + '@q.qq',
        })

        change_email = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            change_email.save()

        expected_raise = {
            'email': [
                'You cannot use this email as a new email.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_CreateChangeEmail_Should_SetPrevEmailFromUser(self):
        data = self.data

        change_email = self.tested_class(**data)
        change_email.save()

        expected_prev_email = self.user.email
        real_prev_email = change_email.prev_email

        expected_email = 'e' * 50 + '@q.qq'
        real_email = change_email.email

        self.assertEqual(expected_prev_email, real_prev_email)
        self.assertEqual(expected_email, real_email)
