from django.db.models import IntegerChoices
from django.test import TestCase

from ...models.QuestionTypeChoices import QuestionTypeChoices


class QuestionTypeChoicesTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = QuestionTypeChoices

    def test_Should_InheritCertainClasses(self):
        expected_classes = (
            IntegerChoices,
        )
        real_classes = self.tested_class.__bases__

        self.assertEqual(expected_classes, real_classes)
