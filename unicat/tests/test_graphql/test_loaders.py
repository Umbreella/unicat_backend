from inspect import getmembers
from unittest import TestCase

from ...graphql import loaders


class LoadersTestCase(TestCase):
    def test_When_CreateNewObjectLoaders_Should_IncludeRequireParams(self):
        expected_params = [
            'answer_value_loader', 'category_loader', 'certificate_loader',
            'course_body_loader', 'discount_loader', 'private_children_loader',
            'public_children_loader', 'teacher_loader', 'user_lesson_loader',
            'user_loader', 'user_progress_loader',
        ]
        real_params = [
            param for param, _ in getmembers(loaders.Loaders())
            if not param.startswith('_')
        ]

        sorted_expected_params = sorted(expected_params)
        sorted_real_params = sorted(real_params)

        self.assertEqual(sorted_expected_params, sorted_real_params)
