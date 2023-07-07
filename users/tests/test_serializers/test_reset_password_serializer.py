from django.core import mail
from django.test import TestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ValidationError

from ...models import User
from ...models.ResetPassword import ResetPassword
from ...serializers.ResetPasswordSerializer import ResetPasswordSerializer


class RegistrationUserSerializerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = ResetPasswordSerializer

        User.objects.create_user(**{
            'email': 'test@email.com',
            'password': 'password',
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
        })

        cls.data = {
            'email': 'test@email.com',
        }

    def test_When_DataIsEmpty_Should_ErrorRequiredFields(self):
        serializer = self.tested_class(data={})

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        excepted_raise = {
            'email': [
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
            'email': '',
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        excepted_errors = {
            'email': [
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
            'email': 'q' * 119 + '@email.com',
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        excepted_errors = {
            'email': [
                ErrorDetail(**{
                    'string': (
                        'Ensure this field has no more than 128 characters.'
                    ),
                    'code': 'max_length',
                }),
            ],
        }
        real_errors = _raise.exception.detail

        self.assertEqual(excepted_errors, real_errors)

    def test_When_UserDoesNotExistInDatabase_Should_DontSentEmail(self):
        data = self.data
        data.update({
            'email': 'test1@email.com',
        })

        serializer = self.tested_class(data=data)
        serializer.is_valid()
        serializer.save()

        expected_count_mail = 0
        real_count_mail = len(mail.outbox)

        self.assertEqual(expected_count_mail, real_count_mail)

    def test_When_UserExistsInDataBase_Should_SentEmail(self):
        data = self.data

        serializer = self.tested_class(data=data)
        serializer.is_valid()
        serializer.save()

        expected_count_mail = 1
        real_count_mail = len(mail.outbox)

        _mail = mail.outbox[0]

        expected_subject = 'Please reset your password'
        real_subject = _mail.subject

        reset_password_url = ResetPassword.objects.last().url
        has_reset_password_url = str(reset_password_url) in _mail.body

        self.assertEqual(expected_count_mail, real_count_mail)
        self.assertEqual(expected_subject, real_subject)
        self.assertTrue(has_reset_password_url)
