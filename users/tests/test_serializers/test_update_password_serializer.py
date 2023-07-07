from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ValidationError

from ...models import User
from ...models.ResetPassword import ResetPassword
from ...serializers.UpdatePasswordSerializer import UpdatePasswordSerializer


class UpdatePasswordSerializerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UpdatePasswordSerializer

        cls.user = User.objects.create_user(**{
            'email': 'test@email.com',
            'password': 'password',
        })

        cls.valid_reset_password = ResetPassword.objects.create(**{
            'user': cls.user,
        })

        cls.not_valid_reset_password = ResetPassword.objects.create(**{
            'user': cls.user,
            'closed_at': timezone.now() - timedelta(minutes=10),
        })

        cls.data = {
            'url': str(cls.valid_reset_password.url),
            'password': 'q' * 50,
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
            'password': [
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
            'password': '',
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
            'password': [
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
            'password': 'q' * 7,
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
            'password': [
                ErrorDetail(**{
                    'string': (
                        'Ensure this field has at least 8 characters.'
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
            'password': 'q' * 129,
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
            'password': [
                ErrorDetail(**{
                    'string': (
                        'Ensure this field has no more than 128 characters.'
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

    def test_When_ResetPasswordEnded_Should_ErrorNotFound(self):
        data = self.data
        data.update({
            'url': str(self.not_valid_reset_password.url),
        })

        serializer = self.tested_class(data=data)
        serializer.is_valid()

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'url': [
                ErrorDetail(**{
                    'string': 'Active password reset request not found.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_ResetPasswordOnUsedPassword_Should_ErrorCantResetPassword(
            self):
        data = self.data
        data.update({
            'password': 'password',
        })

        serializer = self.tested_class(data=data)
        serializer.is_valid()

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'password': [
                ErrorDetail(**{
                    'string': 'This password is already in use.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_ResetPasswordIsActive_Should_UpdateUserPassword(self):
        data = self.data

        serializer = self.tested_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        date_format = '%H-%M %d-%m-%Y'
        self.user.refresh_from_db()
        self.valid_reset_password.refresh_from_db()

        expected_is_active = True
        real_password_is_active = self.user.check_password('q' * 50)

        real_closed_at = self.valid_reset_password.closed_at

        expected_closed_at_str = timezone.now().strftime(date_format)
        real_closed_at_str = real_closed_at.strftime(date_format)

        self.assertEqual(expected_is_active, real_password_is_active)
        self.assertEqual(expected_closed_at_str, real_closed_at_str)
