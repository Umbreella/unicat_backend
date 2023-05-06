from django.test import TestCase
from django_filters import OrderingFilter

from ...filtersets.CategoryFilterSet import CategoryFilterSet
from ...models.Category import Category


class CategoryFilterSetTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CategoryFilterSet

        Category.objects.create(**{
            'title': 'q' * 50,
        })

        Category.objects.create(**{
            'title': 'w' * 50,
        })

        Category.objects.create(**{
            'title': 'e' * 50,
        })

    def test_Should_IncludeDefiniteFilters(self):
        expected_filters = [
            'order_by',
        ]
        real_filters = list(self.tested_class.get_filters())

        self.assertEqual(expected_filters, real_filters)

    def test_Should_SpecificTypeForEachFilter(self):
        expected_filters = {
            'order_by': OrderingFilter,
        }
        real_filters = {
            key: value.__class__
            for key, value in self.tested_class.get_filters().items()
        }

        self.assertEqual(expected_filters, real_filters)

    def test_When_OrderByTitle_Should_ReturnOrderedData(self):
        data = {
            'order_by': 'title',
        }
        base_queryset = Category.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = list(base_queryset.order_by('title'))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_OrderByTitleDesc_Should_ReturnOrderedDescData(self):
        data = {
            'order_by': '-title',
        }
        base_queryset = Category.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = list(base_queryset.order_by('-title'))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)
