from django.db.models import IntegerChoices
from django.test import TestCase

from ...models.CommentedTypeChoices import CommentedTypeChoices


class CommentedTypeChoicesTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CommentedTypeChoices

    def test_Should_InheritCertainClasses(self):
        expected_classes = (
            IntegerChoices,
        )
        real_classes = self.tested_class.__bases__

        self.assertEqual(expected_classes, real_classes)
