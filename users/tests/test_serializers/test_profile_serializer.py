from django.core import mail
from django.test import TestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ValidationError

from ...models import User
from ...models.ChangeEmail import ChangeEmail
from ...serializers.ProfileSerializer import ProfileSerializer


class UpdatePasswordSerializerTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = ProfileSerializer

        cls.user = User.objects.create_user(**{
            'email': 'test@email.com',
            'password': 'password',
        })

        User.objects.create_user(**{
            'email': 'test2@email.com',
            'password': 'password',
        })

        cls.data = {
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'photo': '',
            'current_password': 'password',
            'new_password': 'q' * 50,
        }

    def test_When_DataIsEmpty_Should_ErrorRequiredFields(self):
        serializer = self.tested_class(data={})

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'email': [
                ErrorDetail(**{
                    'string': 'This field is required.',
                    'code': 'required',
                }),
            ],
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
            'photo': [
                ErrorDetail(**{
                    'string': 'No file was submitted.',
                    'code': 'required',
                }),
            ],
            'current_password': [
                ErrorDetail(**{
                    'string': 'This field is required.',
                    'code': 'required',
                }),
            ],
            'new_password': [
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
            'email': '',
            'first_name': '',
            'last_name': '',
            'photo': '',
            'current_password': '',
            'new_password': '',
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'email': [
                ErrorDetail(**{
                    'string': 'This field may not be blank.',
                    'code': 'blank',
                }),
            ],
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
            'current_password': [
                ErrorDetail(**{
                    'string': 'This field may not be blank.',
                    'code': 'blank',
                }),
            ],
            'new_password': [
                ErrorDetail(**{
                    'string': 'This field may not be blank.',
                    'code': 'blank',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataLessThanMinLength_Should_ErrorMinLength(self):
        data = self.data
        data.update({
            'current_password': 'q' * 7,
            'new_password': 'q' * 7,
        })

        serializer = self.tested_class(data=data, partial=True)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'current_password': [
                ErrorDetail(**{
                    'string': (
                        'Ensure this field has at least 8 characters.'
                    ),
                    'code': 'min_length',
                }),
            ],
            'new_password': [
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

    def test_When_DataGreaterThanMaxLength_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'email': 'q' * 120 + '@email.com',
            'first_name': 'q' * 129,
            'last_name': 'q' * 129,
            'current_password': 'q' * 129,
            'new_password': 'q' * 129,
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'email': [
                ErrorDetail(**{
                    'string': (
                        'Ensure this field has no more than 128 characters.'
                    ),
                    'code': 'max_length',
                }),
            ],
            'first_name': [
                ErrorDetail(**{
                    'string': (
                        'Ensure this field has no more than 128 characters.'
                    ),
                    'code': 'max_length',
                }),
            ],
            'last_name': [
                ErrorDetail(**{
                    'string': (
                        'Ensure this field has no more than 128 characters.'
                    ),
                    'code': 'max_length',
                }),
            ],
            'current_password': [
                ErrorDetail(**{
                    'string': (
                        'Ensure this field has no more than 128 characters.'
                    ),
                    'code': 'max_length',
                }),
            ],
            'new_password': [
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

    def test_When_OnlyCurrentPassword_Should_ErrorBothPasswordMustBeFilled(
            self):
        data = self.data
        del data['new_password']

        serializer = self.tested_class(data=data, partial=True)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'current_password': [
                ErrorDetail(**{
                    'string': 'This field must be filled.',
                    'code': 'invalid',
                }),
            ],
            'new_password': [
                ErrorDetail(**{
                    'string': 'This field must be filled.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_OnlyNewPassword_Should_ErrorBothPasswordMustBeFilled(self):
        data = self.data
        del data['current_password']

        serializer = self.tested_class(data=data, partial=True)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'current_password': [
                ErrorDetail(**{
                    'string': 'This field must be filled.',
                    'code': 'invalid',
                }),
            ],
            'new_password': [
                ErrorDetail(**{
                    'string': 'This field must be filled.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_NotValidCurrentPassword_Should_UpdateInstanceButNotPassword(
            self):
        data = self.data
        data.update({
            'current_password': 'password1',
        })

        serializer = self.tested_class(data=data, instance=self.user,
                                       partial=True, )
        serializer.is_valid()

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'current_password': [
                ErrorDetail(**{
                    'string': 'Incorrect password.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_IsValidCurrentPassword_Should_UpdateInstance(self):
        data = self.data

        serializer = self.tested_class(data=data, instance=self.user,
                                       partial=True)
        serializer.is_valid()
        serializer.save()

        expected_data = {
            'email': 'test@email.com',
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'photo': None,
        }
        real_data = serializer.data

        new_password_is_active = self.user.check_password('q' * 50)

        self.assertEqual(expected_data, real_data)
        self.assertTrue(new_password_is_active)

    def test_When_DataWithOutPassword_Should_UpdateInstanceWithOutPassword(
            self):
        data = self.data
        del data['current_password']
        del data['new_password']

        serializer = self.tested_class(data=data, instance=self.user,
                                       partial=True)
        serializer.is_valid()
        serializer.save()

        expected_data = {
            'email': 'test@email.com',
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'photo': None,
        }
        real_data = serializer.data

        new_password_is_active = self.user.check_password('q' * 50)

        self.assertEqual(expected_data, real_data)
        self.assertFalse(new_password_is_active)

    def test_When__Should_(self):
        data = {
            'email': 'test2@email.com',
        }
        serializer = self.tested_class(data=data, instance=self.user,
                                       partial=True)
        serializer.is_valid()

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'email': [
                ErrorDetail(**{
                    'string': 'You cannot use this email as a new email.',
                    'code': 'invalid',
                })
            ]
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_NewEmailAddress_Should_SentEmailAndNotChangeOldAddress(self):
        data = {
            'email': 'test1@email.com',
        }
        serializer = self.tested_class(data=data, instance=self.user,
                                       partial=True)
        serializer.is_valid()
        serializer.save()

        change_email = ChangeEmail.objects.last()

        expected_change_email_user = self.user
        real_change_email_user = change_email.user

        expected_change_email_email = 'test1@email.com'
        real_change_email_email = change_email.email

        expected_count_mail = 1
        real_count_mail = len(mail.outbox)

        email = mail.outbox[0]

        expected_email_subject = 'Please confirm your new email'
        real_email_subject = email.subject

        self.assertEqual(expected_change_email_user, real_change_email_user)
        self.assertEqual(expected_change_email_email, real_change_email_email)
        self.assertEqual(expected_count_mail, real_count_mail)
        self.assertEqual(expected_email_subject, real_email_subject)
