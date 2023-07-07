from django.test import TestCase
from rest_framework.filters import BaseFilterBackend

from ...filtersets.LessonParentFilter import LessonParentFilter
from ...models.Lesson import Lesson


class LessonParentFilterTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LessonParentFilter
        cls.target_database = 'master'
        cls.request = type('request', (object,), {})

    def test_Should_InheritBaseFilterBackend(self):
        expected_super_classes = (
            BaseFilterBackend,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_When_QueryParamParentOnlyIsNone_Should_DontChangeQuerySet(self):
        request = self.request
        request.query_params = {}

        expected_queryset = Lesson.objects.all()
        real_queryset = self.tested_class().filter_queryset(**{
            'request': request,
            'queryset': Lesson.objects.all(),
            'view': None,
        })

        expected_query = expected_queryset.query.get_compiler(
            self.target_database,
        ).as_sql()
        real_query = real_queryset.query.get_compiler(
            self.target_database,
        ).as_sql()

        self.assertEqual(expected_query, real_query)

    def test_When_QueryParamParentOnlyIsNotBool_Should_EmptyQuerySet(self):
        request = self.request
        request.query_params = {
            'parent_only': 'q',
        }

        expected_queryset = Lesson.objects.all()
        real_queryset = self.tested_class().filter_queryset(**{
            'request': request,
            'queryset': Lesson.objects.all(),
            'view': None,
        })

        expected_query = expected_queryset.query.get_compiler(
            self.target_database,
        ).as_sql()
        real_query = real_queryset.query.get_compiler(
            self.target_database,
        ).as_sql()

        self.assertEqual(expected_query, real_query)

    def test_When_QueryParamParentOnlyIs0_Should_DontChangeQuerySet(self):
        request = self.request
        request.query_params = {
            'parent_only': 0,
        }

        expected_queryset = Lesson.objects.all()
        real_queryset = self.tested_class().filter_queryset(**{
            'request': request,
            'queryset': Lesson.objects.all(),
            'view': None,
        })

        expected_query = expected_queryset.query.get_compiler(
            self.target_database,
        ).as_sql()
        real_query = real_queryset.query.get_compiler(
            self.target_database,
        ).as_sql()

        self.assertEqual(expected_query, real_query)

    def test_When_QueryParamParentOnlyIs1_Should_ChangeQuerySet(self):
        request = self.request
        request.query_params = {
            'parent_only': '1',
        }

        expected_queryset = Lesson.objects.filter(**{
            'parent__isnull': True,
        })
        real_queryset = self.tested_class().filter_queryset(**{
            'request': request,
            'queryset': Lesson.objects.all(),
            'view': None,
        })

        expected_query = expected_queryset.query.get_compiler(
            self.target_database,
        ).as_sql()
        real_query = real_queryset.query.get_compiler(
            self.target_database,
        ).as_sql()

        self.assertEqual(expected_query, real_query)
