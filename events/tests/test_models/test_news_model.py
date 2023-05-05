from django.core.exceptions import ValidationError
from django.db.models import (BigAutoField, CharField, DateTimeField,
                              ForeignKey, ImageField, TextField)
from django.test import TestCase
from django.utils import timezone

from users.models import User

from ...models.New import New


class NewsModelTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = New

        user = User.objects.create(**{
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        cls.data = {
            'preview': 'temporary_img',
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'author': user,
        }

        cls.date_format = '%H:%M %d-%m-%Y'

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'id', 'preview', 'title', 'short_description', 'description',
            'author', 'created_at',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'preview': ImageField,
            'title': CharField,
            'short_description': CharField,
            'description': TextField,
            'author': ForeignKey,
            'created_at': DateTimeField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }
        self.maxDiff = None
        self.assertEqual(expected_fields, real_fields)

    def test_When_CreateNewsWithOutData_Should_ErrorBlankField(self):
        news = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            news.save()

        expected_raise = {
            'preview': [
                'This field cannot be blank.',
            ],
            'title': [
                'This field cannot be blank.',
            ],
            'short_description': [
                'This field cannot be blank.',
            ],
            'description': [
                'This field cannot be blank.',
            ],
            'author': [
                'This field cannot be blank.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataLengthGreaterThan255_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'title': 'q' * 275,
            'short_description': 'q' * 275,
        })

        news = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            news.save()

        expected_raise = {
            'short_description': [
                'Ensure this value has at most 255 characters (it has 275).',
            ],
            'title': [
                'Ensure this value has at most 255 characters (it has 275).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SaveNewAndReturnTitleAsStr(self):
        data = self.data

        news = self.tested_class(**data)
        news.save()

        expected_str = news.title
        real_str = str(news)

        self.assertEqual(expected_str, real_str)

    def test_When_DontSetCreatedAt_Should_SaveNewWithCreatedAtNow(self):
        data = self.data

        news = self.tested_class(**data)
        news.save()

        expected_created_at = timezone.now().strftime(self.date_format)
        real_created_at = news.created_at.strftime(self.date_format)

        self.assertEqual(expected_created_at, real_created_at)
