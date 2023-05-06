from rest_framework.serializers import ModelSerializer
from snapshottest.django import TestCase

from ...serializers.FeedbackSerializer import FeedbackSerializer


class FeedbackSerializerTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = FeedbackSerializer

    def test_Should_InheritModelSerializer(self):
        expected_super_classes = (
            ModelSerializer,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_IncludeDefiniteFieldsFromModel(self):
        expected_fields = [
            'id', 'name', 'email', 'body', 'created_at', 'is_closed',
        ]
        real_fields = list(self.tested_class().get_fields())

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificFormatForEachField(self):
        real_repr = repr(self.tested_class())

        self.assertMatchSnapshot(real_repr)

    def test_Should_DontOverrideSuperMethods(self):
        expected_methods = [
            ModelSerializer.save,
            ModelSerializer.create,
            ModelSerializer.update,
        ]
        real_methods = [
            self.tested_class.save,
            self.tested_class.create,
            self.tested_class.update,
        ]

        self.assertEqual(expected_methods, real_methods)
