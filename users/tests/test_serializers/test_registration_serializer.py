from django.test import TestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ValidationError

from ...models import User
from ...serializers.RegistrationUserSerializer import \
    RegistrationUserSerializer


class UserRegistrationSerializerTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email='test@email.com', password='password',
                                 first_name='q' * 50, last_name='q' * 50)

        cls.data = {
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'test@email.com',
            'password': 'password'
        }

    def test_When_EmptyFirstAndLastName_Should_ErrorRequiredFields(self):
        data = self.data
        data.pop('first_name')
        data.pop('last_name')

        serializer = RegistrationUserSerializer(data=data)
        serializer.is_valid()

        excepted_errors = {
            'first_name': [
                ErrorDetail(string='This field is required.', code='required')

            ],
            'last_name': [
                ErrorDetail(string='This field is required.', code='required')
            ],
        }
        real_errors = serializer.errors

        self.assertEqual(excepted_errors, real_errors)

    def test_When_BlankFieldsFirstAndLastName_Should_ErrorBlankFields(self):
        data = self.data
        data.update({
            'first_name': '',
            'last_name': ''
        })

        serializer = RegistrationUserSerializer(data=data)
        serializer.is_valid()

        excepted_errors = {
            'first_name': [
                ErrorDetail(string='This field may not be blank.',
                            code='blank')
            ],
            'last_name': [
                ErrorDetail(string='This field may not be blank.',
                            code='blank')
            ],
        }
        real_errors = serializer.errors

        self.assertEqual(excepted_errors, real_errors)

    def test_When_FieldsLengthGreaterThan128_Should_ErrorNotMaxLength(self):
        data = self.data
        data.update({
            'first_name': 'q' * 129,
            'last_name': 'q' * 129,
        })

        serializer = RegistrationUserSerializer(data=data)
        serializer.is_valid()

        excepted_errors = {
            'first_name': [
                ErrorDetail(string='Ensure this field has no more than 128 '
                                   'characters.',
                            code='max_length')
            ],
            'last_name': [
                ErrorDetail(
                    string='Ensure this field has no more than 128 '
                           'characters.',
                    code='max_length')
            ],
        }
        real_errors = serializer.errors

        self.assertEqual(excepted_errors, real_errors)

    def test_When_DuplicateUserData_Should_ErrorNotCreateUser(self):
        data = self.data

        serializer = RegistrationUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        with self.assertRaises(ValidationError):
            serializer.save()

    def test_When_CorrectNewUserData_Should_ReturnTokensAndCreateUser(self):
        data = self.data
        data.update({
            'email': 'test1@email.com'
        })

        serializer = RegistrationUserSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        new_user = User.objects.last()

        excepted_response = ['refresh', 'access']
        real_response = list(serializer.data.keys())

        excepted_email = data['email']
        real_email = new_user.email

        self.assertEqual(excepted_response, real_response)
        self.assertEqual(excepted_email, real_email)
