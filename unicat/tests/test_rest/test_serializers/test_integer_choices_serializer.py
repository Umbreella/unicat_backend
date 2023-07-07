from rest_framework.serializers import Serializer
from snapshottest.django import TestCase

from ....rest.serializers.IntegerChoicesSerializer import \
    IntegerChoicesSerializer


class IntegerChoicesSerializerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = IntegerChoicesSerializer

    def test_Should_InheritModelSerializer(self):
        expected_super_classes = (
            Serializer,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_IncludeDefiniteFieldsFromUserModel(self):
        expected_fields = [
            'id', 'label',
        ]
        real_fields = list(self.tested_class().get_fields())

        self.assertEqual(expected_fields, real_fields)
