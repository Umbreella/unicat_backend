import jwt
from django.conf import settings
from django.core import mail
from django.test import TestCase
from rest_framework.exceptions import AuthenticationFailed, ErrorDetail
from rest_framework.serializers import ValidationError

from ...models import User
from ...serializers.ConfirmEmailSerializer import ConfirmEmailSerializer


class ConfirmEmailSerializerTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = ConfirmEmailSerializer

        cls.user = User.objects.create_user(**{
            'id': 1,
            'email': 'test@email.com',
            'password': 'password',
        })

        User.objects.create_user(**{
            'id': 2,
            'email': 'test1@email.com',
            'password': 'password',
            'is_active': True,
        })

        cls.data = {
            'url': jwt.encode(**{
                'payload': {
                    'user_id': 1,
                },
                'key': settings.SECRET_KEY,
                'algorithm': 'HS256',
            }),
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
            'url': 'q' * 98,
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'url': [
                ErrorDetail(**{
                    'string': (
                        'Ensure this field has at least 99 characters.'
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
            'url': 'q' * 124,
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'url': [
                ErrorDetail(**{
                    'string': (
                        'Ensure this field has no more than 123 characters.'
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
            'url': 'q' * 100,
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

    def test_When_UserIsNotRegistered_Should_ErrorNotFound(self):
        data = self.data
        data.update({
            'url': jwt.encode(**{
                'payload': {
                    'user_id': 3,
                },
                'key': settings.SECRET_KEY,
                'algorithm': 'HS256',
            }),
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(AuthenticationFailed) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = ErrorDetail(**{
            'string': 'User not found.',
            'code': 'authentication_failed',
        })
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_UserIsActivated_Should_ErrorUserIsVerified(self):
        data = self.data
        data.update({
            'url': jwt.encode(**{
                'payload': {
                    'user_id': 2,
                },
                'key': settings.SECRET_KEY,
                'algorithm': 'HS256',
            }),
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(AuthenticationFailed) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = ErrorDetail(**{
            'string': 'User already verified.',
            'code': 'authentication_failed',
        })
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataIsValid_Should_ChangeIsActiveAndSentMail(self):
        data = self.data

        serializer = self.tested_class(data=data)
        serializer.is_valid()
        serializer.save()

        expected_is_active = True
        real_is_active = serializer.user.is_active

        expected_count_mail = 1
        real_count_mail = len(mail.outbox)

        expected_subject = 'Your registration is complete'
        real_subject = mail.outbox[0].subject

        self.assertEqual(expected_is_active, real_is_active)
        self.assertEqual(expected_count_mail, real_count_mail)
        self.assertEqual(expected_subject, real_subject)
