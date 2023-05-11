from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ValidationError

from ...models import User
from ...models.ChangeEmail import ChangeEmail
from ...serializers.ConfirmNewEmailSerializer import ConfirmNewEmailSerializer


class ConfirmNewEmailSerializerTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = ConfirmNewEmailSerializer

        cls.user = User.objects.create_user(**{
            'email': 'test@email.com',
            'password': 'password',
        })

        cls.valid_change_email = ChangeEmail.objects.create(**{
            'user': cls.user,
            'email': 'test1@email.com',
        })

        cls.not_valid_change_email = ChangeEmail.objects.create(**{
            'user': cls.user,
            'email': 'test1@email.com',
            'closed_at': timezone.now() - timedelta(minutes=10),
        })

        cls.data = {
            'url': str(cls.valid_change_email.url),
        }

    def test_When_DataIsEmpty_Should_ErrorRequiredFields(self):
        serializer = self.tested_class(data={})

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'url': [
                ErrorDetail(**{
                    'string': 'This field is required.',
                    'code': 'required',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_FieldsIsEmpty_Should_ErrorBlankFields(self):
        data = self.data
        data.update({
            'url': '',
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'url': [
                ErrorDetail(**{
                    'string': 'This field may not be blank.',
                    'code': 'blank',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataIsLessThanMinLength_Should_ErrorMinLength(self):
        data = self.data
        data.update({
            'url': 'q' * 35,
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'url': [
                ErrorDetail(**{
                    'string': (
                        'Ensure this field has at least 36 characters.'
                    ),
                    'code': 'min_length',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataIsGreaterThanMinLength_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'url': 'q' * 37,
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'url': [
                ErrorDetail(**{
                    'string': (
                        'Ensure this field has no more than 36 characters.'
                    ),
                    'code': 'max_length',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_UrlIsRandomString_Should_ErrorNotValidField(self):
        data = self.data
        data.update({
            'url': 'q' * 36,
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'url': [
                ErrorDetail(**{
                    'string': 'This field is not valid.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_ChangeEmailEnded_Should_ErrorNotFound(self):
        data = self.data
        data.update({
            'url': str(self.not_valid_change_email.url),
        })

        serializer = self.tested_class(data=data)
        serializer.is_valid()

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'url': [
                ErrorDetail(**{
                    'string': 'Value not found.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_ChangeEmailIsActive_Should_UpdateUserPassword(self):
        data = self.data

        serializer = self.tested_class(data=data)
        serializer.is_valid()
        serializer.save()

        date_format = '%H-%M %d-%m-%Y'
        self.user.refresh_from_db()
        self.valid_change_email.refresh_from_db()

        expected_email = 'test1@email.com'
        real_email = self.user.email

        expected_closed_at = timezone.now()
        real_closed_at = self.valid_change_email.closed_at

        expected_closed_at_str = expected_closed_at.strftime(date_format)
        real_closed_at_str = real_closed_at.strftime(date_format)

        self.assertEqual(expected_email, real_email)
        self.assertEqual(expected_closed_at_str, real_closed_at_str)
