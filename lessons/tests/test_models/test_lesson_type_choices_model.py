from django.db.models import IntegerChoices
from django.test import TestCase

from ...models.LessonTypeChoices import LessonTypeChoices


class LessonTypeChoicesTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LessonTypeChoices

    def test_Should_InheritCertainClasses(self):
        expected_classes = (
            IntegerChoices,
        )
        real_classes = self.tested_class.__bases__

        self.assertEqual(expected_classes, real_classes)
