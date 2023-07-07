from django.db.models import IntegerChoices
from django.test import TestCase

from ...models.LearningFormat import LearningFormat


class LearningFormatTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LearningFormat

    def test_Should_InheritCertainClasses(self):
        expected_classes = (
            IntegerChoices,
        )
        real_classes = self.tested_class.__bases__

        self.assertEqual(expected_classes, real_classes)
