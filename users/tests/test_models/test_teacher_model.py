from django.core.exceptions import ValidationError
from django.db.models import (BigAutoField, CharField, DecimalField,
                              ManyToOneRel, OneToOneField,
                              PositiveIntegerField)
from django.test import TestCase

from ...models import User
from ...models.Teacher import Teacher


class UserModelTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Teacher

        user = User.objects.create(**{
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
            'photo': 'temporary_img',
        })

        cls.data = {
            'user': user,
            'description': 'q' * 50,
            'avg_rating': 1.0,
            'count_reviews': 1,
            'facebook': 'q' * 50,
            'twitter': 'q' * 50,
            'google_plus': 'q' * 50,
            'vk': 'q' * 50,
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'course',
            'id',
            'user',
            'description',
            'avg_rating',
            'count_reviews',
            'facebook',
            'twitter',
            'google_plus',
            'vk',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'course': ManyToOneRel,
            'id': BigAutoField,
            'user': OneToOneField,
            'description': CharField,
            'avg_rating': DecimalField,
            'count_reviews': PositiveIntegerField,
            'facebook': CharField,
            'twitter': CharField,
            'google_plus': CharField,
            'vk': CharField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'course': '',
            'id': '',
            'user': 'User for whom the teacher record is added.',
            'description': 'Some words about teacher.',
            'avg_rating': 'Average rating from all teachers courses.',
            'count_reviews': (
                'The total number of all reviews left by users for all '
                'courses of this teacher.'
            ),
            'facebook': 'Link to the user`s Facebook page.',
            'twitter': 'Link to the user`s Twitter page.',
            'google_plus': 'Link to the user`s GooglePlus page.',
            'vk': 'Link to the user`s VK page.',
        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreateTeacherWithOutData_Should_ErrorBlankField(self):
        teacher = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            teacher.save()

        expected_raise = {
            'description': [
                'This field cannot be blank.',
            ],
            'user': [
                'This field cannot be null.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_LengthDataGreaterThan255_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'description': 'q' * 275,
            'facebook': 'q' * 275,
            'twitter': 'q' * 275,
            'google_plus': 'q' * 275,
            'vk': 'q' * 275,
        })

        teacher = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            teacher.save()

        expected_raise = {
            'description': [
                'Ensure this value has at most 255 characters (it has 275).',
            ],
            'facebook': [
                'Ensure this value has at most 255 characters (it has 275).',
            ],
            'twitter': [
                'Ensure this value has at most 255 characters (it has 275).',
            ],
            'google_plus': [
                'Ensure this value has at most 255 characters (it has 275).',
            ],
            'vk': [
                'Ensure this value has at most 255 characters (it has 275).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_TeacherWithOutLinks_Should_CreateTeacherAndReturnUser(self):
        data = self.data
        data.pop('facebook')
        data.pop('twitter')
        data.pop('google_plus')
        data.pop('vk')

        teacher = self.tested_class(**data)
        teacher.save()

        expected_str = str(teacher.user)
        real_str = str(teacher)

        self.assertEqual(expected_str, real_str)
