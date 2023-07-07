from django.test import TestCase
from rest_framework.pagination import PageNumberPagination

from ....rest.pagination.DynamicPagination import DynamicPagination


class DynamicPaginationTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = DynamicPagination

    def test_Should_InheritPageNumberPagination(self):
        expected_super_classes = (
            PageNumberPagination,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_PageSizeSetOn25(self):
        expected_page_size = 25
        real_page_size = self.tested_class.page_size

        self.assertEqual(expected_page_size, real_page_size)

    def test_Should_PageSizeQueryParamsSetOnPageSize(self):
        expected_query_param = 'page_size'
        real_query_param = self.tested_class.page_size_query_param

        self.assertEqual(expected_query_param, real_query_param)

    def test_Should_MaxPageSizeSetOn50(self):
        expected_max_page_size = 50
        real_max_page_size = self.tested_class.max_page_size

        self.assertEqual(expected_max_page_size, real_max_page_size)
