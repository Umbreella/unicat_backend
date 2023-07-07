from django.core.exceptions import ValidationError
from django.db.models import (BigAutoField, BooleanField, CharField,
                              DateTimeField, EmailField, ImageField,
                              ManyToManyField, ManyToManyRel, ManyToOneRel,
                              OneToOneRel)
from django.test import TestCase

from ...models import User


class UserModelTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = User

        cls.data = {
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'logentry', 'outstandingtoken', 'my_courses', 'my_progress',
            'comment', 'new', 'my_lessons', 'userlesson', 'payments',
            'teacher', 'resetpassword', 'changeemail', 'id', 'last_login',
            'is_superuser', 'email', 'password', 'first_name', 'last_name',
            'photo', 'is_staff', 'is_active', 'groups', 'user_permissions',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'logentry': ManyToOneRel,
            'outstandingtoken': ManyToOneRel,
            'my_courses': ManyToManyRel,
            'my_progress': ManyToOneRel,
            'comment': ManyToOneRel,
            'new': ManyToOneRel,
            'my_lessons': ManyToManyRel,
            'userlesson': ManyToOneRel,
            'payments': ManyToOneRel,
            'resetpassword': ManyToOneRel,
            'teacher': OneToOneRel,
            'changeemail': ManyToOneRel,
            'id': BigAutoField,
            'last_login': DateTimeField,
            'is_superuser': BooleanField,
            'email': EmailField,
            'password': CharField,
            'first_name': CharField,
            'last_name': CharField,
            'photo': ImageField,
            'is_staff': BooleanField,
            'is_active': BooleanField,
            'groups': ManyToManyField,
            'user_permissions': ManyToManyField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'logentry': '',
            'outstandingtoken': '',
            'my_courses': '',
            'my_progress': '',
            'comment': '',
            'new': '',
            'my_lessons': '',
            'userlesson': '',
            'payments': '',
            'resetpassword': '',
            'teacher': '',
            'changeemail': '',
            'id': '',
            'last_login': '',
            'is_superuser': (
                'Designates that this user has all permissions without '
                'explicitly assigning them.'
            ),
            'email': 'User`s unique email address.',
            'password': 'User password.',
            'first_name': 'Username.',
            'last_name': 'User`s last name.',
            'photo': 'User Image.',
            'is_staff': (
                'Does the user have access to the administration panel.'
            ),
            'is_active': 'Is this account active.',
            'groups': (
                'The groups this user belongs to. A user will get all '
                'permissions granted to each of their groups.'
            ),
            'user_permissions': 'Specific permissions for this user.',
        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreateUserWithOutData_Should_ErrorBlankField(self):
        user = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            user.save()

        expected_raise = {
            'email': [
                'This field cannot be blank.',
            ],
            'password': [
                'This field cannot be blank.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_LengthDataGreaterThan128_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'first_name': 'q' * 130,
            'last_name': 'q' * 130,
            'email': 'q' * 125 + '@q.qq',
            'password': 'q' * 130,
        })

        user = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            user.save()

        expected_raise = {
            'first_name': [
                'Ensure this value has at most 128 characters (it has 130).',
            ],
            'last_name': [
                'Ensure this value has at most 128 characters (it has 130).',
            ],
            'email': [
                'Ensure this value has at most 128 characters (it has 130).',
            ],
            'password': [
                'Ensure this value has at most 128 characters (it has 130).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_EmailIsNotValid_Should_ErrorInvalidValue(self):
        data = self.data
        data.update({
            'email': 'q' * 50
        })

        user = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            user.save()

        expected_raise = {
            'email': [
                'Enter a valid email address.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SaveUserAndReturnFullNameAsStr(self):
        data = self.data

        user = self.tested_class(**data)
        user.save()

        expected_str = f'{user.first_name} {user.last_name}'
        real_str = str(user)

        self.assertEqual(expected_str, real_str)

    def test_When_NamesIsNull_Should_ReturnEmailAsFullName(self):
        data = self.data
        data.pop('first_name')
        data.pop('last_name')

        user = self.tested_class(**data)
        user.save()

        expected_str = user.email
        real_str = str(user)

        self.assertEqual(expected_str, real_str)

    def test_When_DuplicateUserEmail_Should_ErrorDuplicateUser(self):
        data = self.data

        user = self.tested_class(**data)
        user.save()

        duplicate_user = User(**data)

        with self.assertRaises(ValidationError) as _raise:
            duplicate_user.save()

        expected_raise = {
            'email': [
                'User with this Email already exists.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_UseCreateUserFromObjectManager_Should_SaveUser(self):
        data = self.data

        user = self.tested_class.objects.create_user(**data)
        user.save()

        expected_is_staff = False
        real_is_staff = user.is_staff

        expected_is_superuser = False
        real_is_superuser = user.is_superuser

        expected_is_active = False
        real_is_active = user.is_active

        self.assertEqual(expected_is_staff, real_is_staff)
        self.assertEqual(expected_is_superuser, real_is_superuser)
        self.assertEqual(expected_is_active, real_is_active)

    def test_When_UseCreateSuperUserFromObjectManager_Should_SaveUserAsAdmin(
            self
    ):
        data = self.data

        user = self.tested_class.objects.create_superuser(**data)
        user.save()

        expected_is_staff = True
        real_is_staff = user.is_staff

        expected_is_superuser = True
        real_is_superuser = user.is_superuser

        expected_is_active = True
        real_is_active = user.is_active

        self.assertEqual(expected_is_staff, real_is_staff)
        self.assertEqual(expected_is_superuser, real_is_superuser)
        self.assertEqual(expected_is_active, real_is_active)
