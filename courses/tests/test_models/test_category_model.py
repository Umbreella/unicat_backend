from django.core.exceptions import ValidationError
from django.db.models import BigAutoField, CharField, ManyToOneRel
from django.test import TestCase

from ...models.Category import Category


class CategoryModelTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Category

        cls.data = {
            'title': 'q' * 50,
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'courses', 'id', 'title',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'courses': ManyToOneRel,
            'id': BigAutoField,
            'title': CharField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_When_CreateCategoryWithOutTitle_Should_ErrorBlankField(self):
        category = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            category.save()

        expected_raise = {
            'title': [
                'This field cannot be blank.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_TitleLengthGreaterThan128_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'title': 'q' * 130,
        })

        category = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            category.save()

        expected_raise = {
            'title': [
                'Ensure this value has at most 128 characters (it has 130).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SaveCategoryAndReturnTitle(
            self):
        data = self.data

        category = self.tested_class(**data)
        category.save()

        expected_str = category.title
        real_str = str(category)

        self.assertEqual(expected_str, real_str)
