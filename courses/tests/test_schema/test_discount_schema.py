from django.test import TestCase
from graphene import NonNull
from graphene.utils.subclass_with_meta import SubclassWithMeta_Meta

from ...models.Discount import Discount
from ...schema.DiscountType import DiscountType


class DiscountTypeTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = DiscountType
        cls.model = Discount

    def test_Should_IncludeDefiniteDjangoModel(self):
        expected_model = self.model
        real_model = self.tested_class._meta.model

        self.assertEqual(expected_model, real_model)

    def test_Should_IncludeDefiniteInterfaces(self):
        expected_interfaces = []
        real_interfaces = list(self.tested_class._meta.interfaces)

        self.assertEqual(expected_interfaces, real_interfaces)

    def test_Should_IncludeAllFieldsFromModel(self):
        expected_fields = (
            'percent', 'end_date',
        )
        real_fields = tuple(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'percent': NonNull,
            'end_date': SubclassWithMeta_Meta,
        }
        real_fields = {
            key: value.type.__class__
            for key, value in self.tested_class._meta.fields.items()
        }

        self.assertEqual(expected_fields, real_fields)
