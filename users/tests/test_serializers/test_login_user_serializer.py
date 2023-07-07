from django.test import TestCase
from rest_framework.exceptions import (AuthenticationFailed, ErrorDetail,
                                       ValidationError)

from ...models import User
from ...serializers.LoginUserSerializer import LoginUserSerializer


class LoginUserSerializerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LoginUserSerializer

        cls.not_active_user = {
            'email': 'test@email.com',
            'password': 'password',
        }

        cls.active_user = {
            'email': 'test1@email.com',
            'password': 'password',
        }

        User.objects.create_user(**cls.not_active_user)
        User.objects.create_user(**{
            **cls.active_user,
            'is_active': True,
        })

    def test_When_EmptyData_Should_ErrorRequiredFields(self):
        data = {}

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_errors = {
            'email': [
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
        real_errors = _raise.exception.detail

        self.assertEqual(expected_errors, real_errors)

    def test_When_EmptyFields_Should_ErrorBlankFields(self):
        data = {
            'email': '',
            'password': '',
        }

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_errors = {
            'email': [
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
        real_errors = _raise.exception.detail

        self.assertEqual(expected_errors, real_errors)

    def test_When_BadEmail_Should_ErrorNotValidateEmail(self):
        data = {
            'email': 'qwer',
            'password': 'qwer',
        }

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_errors = {
            'email': [
                ErrorDetail(**{
                    'string': 'Enter a valid email address.',
                    'code': 'invalid',
                }),
            ],
        }
        real_errors = _raise.exception.detail

        self.assertEqual(expected_errors, real_errors)

    def test_When_DataGreaterThanMaxLength_Should_ErrorMaxLength(self):
        data = {
            'email': 'q' * 124 + '@a.ru',
            'password': 'q' * 129,
        }

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_errors = {
            'email': [
                ErrorDetail(**{
                    'string': 'Ensure this field has no more than 128 '
                              'characters.',
                    'code': 'max_length',
                }),
            ],
            'password': [
                ErrorDetail(**{
                    'string': 'Ensure this field has no more than 128 '
                              'characters.',
                    'code': 'max_length',
                }),
            ],
        }
        real_errors = _raise.exception.detail

        self.assertEqual(expected_errors, real_errors)

    def test_When_RandomUserData_Should_ErrorUserNotFound(self):
        data = {
            'email': 'qwer@qwer.qwer',
            'password': 'qwer',
        }

        serializer = self.tested_class(data=data)

        with self.assertRaises(AuthenticationFailed) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = [
            ErrorDetail(**{
                'string': 'User not found.',
                'code': 'authentication_failed',
            }),
        ]
        real_raise = [_raise.exception.detail]

        self.assertEqual(expected_raise, real_raise)

    def test_When_CorrectUserDataButUserNotActive_Should_ErrorAuthFailed(self):
        data = self.not_active_user

        serializer = self.tested_class(data=data)

        with self.assertRaises(AuthenticationFailed) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = [
            ErrorDetail(**{
                'string': 'User not found.',
                'code': 'authentication_failed',
            }),
        ]
        real_raise = [_raise.exception.detail]

        self.assertEqual(expected_raise, real_raise)

    def test_When_CorrectUserDataAndUserActive_Should_ErrorAuthFailed(self):
        data = self.active_user

        serializer = self.tested_class(data=data)
        serializer.is_valid()

        expected_response = ['refresh', 'access']
        real_response = list(serializer.data.keys())

        self.assertEqual(expected_response, real_response)
