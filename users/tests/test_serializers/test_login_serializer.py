from django.test import TestCase
from rest_framework.exceptions import AuthenticationFailed, ErrorDetail

from ...models import User
from ...serializers.LoginUserSerializer import LoginUserSerializer


class UserLoginSerializerTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email='test@email.com', password='password')

    def test_When_EmptyData_Should_ErrorRequiredFields(self):
        data = {}

        serializer = LoginUserSerializer(data=data)
        serializer.is_valid()

        expected_errors = {
            'email': [
                ErrorDetail(string='This field is required.', code='required')
            ],
            'password': [
                ErrorDetail(string='This field is required.', code='required')
            ]
        }
        real_errors = serializer.errors

        self.assertEqual(expected_errors, real_errors)

    def test_When_EmptyFields_Should_ErrorBlankFields(self):
        data = {
            'email': '',
            'password': ''
        }

        serializer = LoginUserSerializer(data=data)
        serializer.is_valid()

        expected_errors = {
            'email': [
                ErrorDetail(string='This field may not be blank.',
                            code='blank')
            ],
            'password': [
                ErrorDetail(string='This field may not be blank.',
                            code='blank')
            ]
        }
        real_errors = serializer.errors

        self.assertEqual(expected_errors, real_errors)

    def test_When_BadEmail_Should_ErrorNotValidateEmail(self):
        data = {
            'email': 'qwer',
            'password': 'qwer'
        }

        serializer = LoginUserSerializer(data=data)
        serializer.is_valid()

        expected_errors = {
            'email': [
                ErrorDetail(string='Enter a valid email address.',
                            code='invalid')
            ],
        }
        real_errors = serializer.errors

        self.assertEqual(expected_errors, real_errors)

    def test_When_FiledsLengthGreaterThan128_Should_ErrorMaxLength(self):
        data = {
            'email': 'q' * 124 + '@a.ru',
            'password': 'q' * 129
        }

        serializer = LoginUserSerializer(data=data)
        serializer.is_valid()

        expected_errors = {
            'email': [
                ErrorDetail(string='Ensure this field has no more than 128 '
                                   'characters.',
                            code='max_length')
            ],
            'password': [
                ErrorDetail(
                    string='Ensure this field has no more than 128 '
                           'characters.',
                    code='max_length')
            ],
        }
        real_errors = serializer.errors

        self.assertEqual(expected_errors, real_errors)

    def test_When_RandomUserData_Should_ErrorUserNotFound(self):
        data = {
            'email': 'qwer@qwer.qwer',
            'password': 'qwer'
        }

        serializer = LoginUserSerializer(data=data)

        with self.assertRaises(AuthenticationFailed):
            serializer.is_valid(raise_exception=True)

    def test_When_CorrectUserData_Should_ReturnTokens(self):
        data = {
            'email': 'test@email.com',
            'password': 'password'
        }

        serializer = LoginUserSerializer(data=data)
        serializer.is_valid()

        expected_response = ['refresh', 'access']
        real_response = list(serializer.data.keys())

        self.assertEqual(expected_response, real_response)
