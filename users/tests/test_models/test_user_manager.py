from django.test import TestCase

from ...models import User
from ...models.UserManager import UserManager


class UserManagerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserManager()
        cls.tested_class.model = User

    def test_When_CallCreateUser_Should_CreateSimpleUser(self):
        user = self.tested_class.create_user(**{
            'email': 'user@user.user',
            'password': 'user',
        })

        expected_is_staff = False
        real_is_staff = user.is_staff

        expected_is_superuser = False
        real_is_superuser = user.is_superuser

        self.assertEqual(expected_is_staff, real_is_staff)
        self.assertEqual(expected_is_superuser, real_is_superuser)

    def test_When_CallCreateSuperUser_Should_CreateAdminUser(self):
        user = self.tested_class.create_superuser(**{
            'email': 'user@user.user',
            'password': 'user',
        })

        expected_is_staff = True
        real_is_staff = user.is_staff

        expected_is_superuser = True
        real_is_superuser = user.is_superuser

        self.assertEqual(expected_is_staff, real_is_staff)
        self.assertEqual(expected_is_superuser, real_is_superuser)
