from django.test import TestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ValidationError

from ...models import User
from ...serializers.ChangeDataUserSerializer import ChangeDataUserSerializer


class UserChangeDataSerializerTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create_user(email='user_1@email.com',
                                              password='password',
                                              first_name='q' * 50,
                                              last_name='q' * 50)

        cls.user_2 = User.objects.create_user(email='user_2@email.com',
                                              password='password',
                                              first_name='w' * 50,
                                              last_name='w' * 50)

    def test_When_EmptyFields_Should_ErrorBlankFields(self):
        data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': ''
        }
        current_user = self.user_1

        serializer = ChangeDataUserSerializer(current_user, data=data,
                                              partial=True)
        serializer.is_valid()

        excepted_errors = {
            'email': [
                ErrorDetail(string='This field may not be blank.',
                            code='blank')
            ],
            'password': [
                ErrorDetail(string='This field may not be blank.',
                            code='blank')
            ],
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

    def test_When_FiledsLengthGreaterThan128_Should_ErrorMaxLength(self):
        data = {
            'first_name': 'w' * 129,
            'last_name': 'w' * 129,
            'email': 'w' * 124 + '@a.ru',
            'password': 'w' * 129
        }
        current_user = self.user_1

        serializer = ChangeDataUserSerializer(current_user, data=data,
                                              partial=True)
        serializer.is_valid()

        excepted_errors = {
            'email': [
                ErrorDetail(string='Ensure this field has no more than 128 '
                                   'characters.',
                            code='max_length')
            ],
            'password': [
                ErrorDetail(string='Ensure this field has no more than 128 '
                                   'characters.',
                            code='max_length')
            ],
            'first_name': [
                ErrorDetail(string='Ensure this field has no more than 128 '
                                   'characters.',
                            code='max_length')
            ],
            'last_name': [
                ErrorDetail(string='Ensure this field has no more than 128 '
                                   'characters.',
                            code='max_length')
            ],
        }
        real_errors = serializer.errors

        self.assertEqual(excepted_errors, real_errors)

    def test_When_DuplicateEmail_Should_DontUpdateDataUser(self):
        data = {
            'email': self.user_2.email
        }
        current_user = self.user_1

        serializer = ChangeDataUserSerializer(current_user, data=data,
                                              partial=True)
        serializer.is_valid()

        with self.assertRaises(ValidationError):
            serializer.save()

    def test_When_NewUserEmail_Should_UpdateOnlyUserEmail(self):
        data = {
            'email': 'w' * 50 + '@admin.com'
        }
        current_user = self.user_1

        serializer = ChangeDataUserSerializer(current_user, data=data,
                                              partial=True)
        serializer.is_valid()
        serializer.save()

        excepted_email = data['email']
        real_email = current_user.email

        self.assertEqual(excepted_email, real_email)

    def test_When_NewUserPassword_Should_UpdateOnlyUserPassword(self):
        data = {
            'password': 'w' * 50
        }
        current_user = self.user_1
        expected_password = current_user.password

        serializer = ChangeDataUserSerializer(current_user, data=data,
                                              partial=True)
        serializer.is_valid()
        serializer.save()

        real_password = current_user.password

        self.assertNotEqual(expected_password, real_password)

    def test_When_NewUserFirstname_Should_UpdateOnlyUserFirstname(self):
        data = {
            'first_name': 'w' * 50
        }
        current_user = self.user_1

        serializer = ChangeDataUserSerializer(current_user, data=data,
                                              partial=True)
        serializer.is_valid()
        serializer.save()

        excepted_first_name = data['first_name']
        real_first_name = current_user.first_name

        self.assertEqual(excepted_first_name, real_first_name)

    def test_When_NewUserLastname_Should_UpdateOnlyUserLastname(self):
        data = {
            'last_name': 'w' * 50
        }
        current_user = self.user_1

        serializer = ChangeDataUserSerializer(current_user, data=data,
                                              partial=True)
        serializer.is_valid()
        serializer.save()

        excepted_last_name = data['last_name']
        real_last_name = current_user.last_name

        self.assertEqual(excepted_last_name, real_last_name)

    def test_When_ValidateNewUserData_Should_UpdateUserData(self):
        data = {
            'first_name': 'w' * 50,
            'last_name': 'w' * 50,
            'email': 'test1@email.com',
            'password': 'password1'
        }
        current_user = self.user_1
        expected_password = current_user.password

        serializer = ChangeDataUserSerializer(current_user, data=data,
                                              partial=True)
        serializer.is_valid()
        serializer.save()

        excepted_email = data['email']
        real_email = current_user.email

        excepted_first_name = data['first_name']
        real_first_name = current_user.first_name

        excepted_last_name = data['last_name']
        real_last_name = current_user.last_name

        real_password = current_user.password

        self.assertEqual(excepted_email, real_email)
        self.assertEqual(excepted_first_name, real_first_name)
        self.assertEqual(excepted_last_name, real_last_name)
        self.assertNotEqual(expected_password, real_password)
