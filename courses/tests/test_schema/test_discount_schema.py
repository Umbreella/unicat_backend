from django.test import TestCase
from graphene import NonNull

from ...schema.DiscountType import DiscountType


class DiscountTypeTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = DiscountType

    def test_Should_IncludeAllFieldsFromModel(self):
        expected_fields = (
            'percent', 'end_date',
        )
        real_fields = tuple(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'percent': NonNull,
            'end_date': NonNull,
        }
        real_fields = {
            key: value.type.__class__
            for key, value in self.tested_class._meta.fields.items()
        }

        self.assertEqual(expected_fields, real_fields)
