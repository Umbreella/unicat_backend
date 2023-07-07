from django.test import TestCase
from graphene import relay

from ...nodes.LessonTypeNode import LessonTypeNode
from ...schema.LessonType import LessonType


class LessonTypeNodeTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LessonTypeNode
        cls.expected_type = LessonType

    def test_Should_InheritCertainClasses(self):
        expected_classes = (
            relay.Node,
        )
        real_classes = self.tested_class.__bases__

        self.assertEqual(expected_classes, real_classes)

    def test_Should_OverrideSuperMethod(self):
        expected_method = relay.Node.to_global_id
        real_method = self.tested_class.to_global_id

        self.assertNotEqual(expected_method, real_method)

    def test_When_UseMethod_Should_ReturnOnlyLessonTypeId(self):
        expected_data = 'TGVzc29uVHlwZTox'
        first_data = self.tested_class.to_global_id(None, 1)
        second_data = self.tested_class.to_global_id(1, 1)

        self.assertEqual(expected_data, first_data, second_data)
