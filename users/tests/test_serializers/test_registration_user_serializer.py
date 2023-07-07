from django.core import mail
from django.test import TestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ValidationError

from ...models import User
from ...serializers.RegistrationUserSerializer import \
    RegistrationUserSerializer


class RegistrationUserSerializerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = RegistrationUserSerializer

        User.objects.create_user(**{
            'email': 'test@email.com',
            'password': 'password',
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
        })

        cls.data = {
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'test1@email.com',
            'password': 'password',
        }

    def test_When_EmptyFirstAndLastName_Should_ErrorRequiredFields(self):
        data = self.data
        data.pop('first_name')
        data.pop('last_name')

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        excepted_raise = {
            'first_name': [
                ErrorDetail(**{
                    'string': 'This field is required.',
                    'code': 'required',
                }),
            ],
            'last_name': [
                ErrorDetail(**{
                    'string': 'This field is required.',
                    'code': 'required',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(excepted_raise, real_raise)

    def test_When_BlankFieldsFirstAndLastName_Should_ErrorBlankFields(self):
        data = self.data
        data.update({
            'first_name': '',
            'last_name': ''
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        excepted_errors = {
            'first_name': [
                ErrorDetail(**{
                    'string': 'This field may not be blank.',
                    'code': 'blank',
                }),
            ],
            'last_name': [
                ErrorDetail(**{
                    'string': 'This field may not be blank.',
                    'code': 'blank',
                }),
            ],
        }
        real_errors = _raise.exception.detail

        self.assertEqual(excepted_errors, real_errors)

    def test_When_FieldsLengthGreaterThan128_Should_ErrorNotMaxLength(self):
        data = self.data
        data.update({
            'first_name': 'q' * 129,
            'last_name': 'q' * 129,
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        excepted_errors = {
            'first_name': [
                ErrorDetail(**{
                    'string': 'Ensure this field has no more than 128 '
                              'characters.',
                    'code': 'max_length',
                }),
            ],
            'last_name': [
                ErrorDetail(**{
                    'string': 'Ensure this field has no more than 128 '
                              'characters.',
                    'code': 'max_length',
                }),
            ],
        }
        real_errors = _raise.exception.detail

        self.assertEqual(excepted_errors, real_errors)

    def test_When_DuplicateUserData_Should_ErrorNotCreateUser(self):
        data = self.data
        data.update({
            'email': 'test@email.com',
        })

        serializer = self.tested_class(data=data)
        serializer.is_valid()

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'email': [
                ErrorDetail(**{
                    'string': 'This email is already registered.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_CorrectNewUserData_Should_ReturnTokensAndCreateUser(self):
        data = self.data

        serializer = self.tested_class(data=data)
        serializer.is_valid()
        serializer.save()

        expected_count_mail = 1
        real_count_mail = len(mail.outbox)

        expected_subject = 'Please confirm your email'
        real_subject = mail.outbox[0].subject

        self.assertEqual(expected_count_mail, real_count_mail)
        self.assertEqual(expected_subject, real_subject)
