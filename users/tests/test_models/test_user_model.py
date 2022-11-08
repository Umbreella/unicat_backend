from django.core.exceptions import ValidationError
from django.test import TestCase

from ...models import User


class UserModelTest(TestCase):
    databases = {'master'}

    def test_When_PasswordLengthGreaterThan128_Should_DontSaveUser(self):
        user = User(password='q' * 130, email='test@test.test')

        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_When_EmailNotIsValid_Should_DontSaveUser(self):
        user = User(password='q' * 50, email='testtesttest')

        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_When_EmailLengthGreater128_Should_DontSaveUser(self):
        user = User(password='q' * 50, email='test' * 124 + '@ad.a')

        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_When_AllUserDataIsValid_Should_SaveUserAndReturnEmailAsStr(self):
        user = User(password='q' * 50, email='test@test.test')

        user.full_clean()
        self.assertEqual('test@test.test', str(user))

    def test_When_DuplicateEmail_Should_DontSaveDuplicateUser(self):
        user = User(password='q' * 50, email='test@test.test')
        user.save()

        duplicate_user = User(password='q' * 50, email='test@test.test')

        with self.assertRaises(ValidationError):
            duplicate_user.full_clean()
