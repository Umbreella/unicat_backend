from django.core.exceptions import ValidationError
from django.test import TestCase

from ...models import User


class TeacherModelTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.data = {
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        }

    def test_When_CreateUserWithOutData_Should_ErrorBlankField(self):
        user = User()

        with self.assertRaises(ValidationError) as _raise:
            user.save()

        expected_raise = {
            'email': ['This field cannot be blank.'],
            'password': ['This field cannot be blank.'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_LengthDataGreaterThan128_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'first_name': 'q' * 130,
            'last_name': 'q' * 130,
            'email': 'q' * 125 + '@q.qq',
            'password': 'q' * 130,
        })

        user = User(**data)

        with self.assertRaises(ValidationError) as _raise:
            user.save()

        expected_raise = {
            'first_name': [
                'Ensure this value has at most 128 characters (it has 130).'],
            'last_name': [
                'Ensure this value has at most 128 characters (it has 130).'],
            'email': [
                'Ensure this value has at most 128 characters (it has 130).'],
            'password': [
                'Ensure this value has at most 128 characters (it has 130).'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_EmailIsNotValid_Should_ErrorInvalidValue(self):
        data = self.data
        data.update({
            'email': 'q' * 50
        })

        user = User(**data)

        with self.assertRaises(ValidationError) as _raise:
            user.save()

        expected_raise = {
            'email': ['Enter a valid email address.'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SaveUserAndReturnFullNameAsStr(self):
        data = self.data

        user = User(**data)
        user.save()

        expected_fullname = f'{user.first_name} {user.last_name}'
        real_fullname = user.get_fullname()

        expected_str = user.get_fullname()
        real_str = str(user)

        self.assertEqual(expected_fullname, real_fullname)
        self.assertEqual(expected_str, real_str)

    def test_When_NamesIsNull_Should_ReturnEmailAsFullName(self):
        data = self.data
        data.pop('first_name')
        data.pop('last_name')

        user = User(**data)
        user.save()

        expected_str = user.email
        real_str = str(user)

        self.assertEqual(expected_str, real_str)

    def test_When_DuplicateUserEmail_Should_ErrorDuplicateUser(self):
        data = self.data

        user = User(**data)
        user.save()

        duplicate_user = User(**data)

        with self.assertRaises(ValidationError) as _raise:
            duplicate_user.save()

        expected_raise = {
            'email': ['User with this Email already exists.'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)
