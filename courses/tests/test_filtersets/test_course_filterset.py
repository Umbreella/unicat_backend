from django.test import TestCase
from django_filters import CharFilter, NumberFilter, OrderingFilter
from graphql import GraphQLError

from users.models import User
from users.models.Teacher import Teacher

from ...filtersets.CourseFilterSet import CourseFilterSet
from ...models.Category import Category
from ...models.Course import Course
from ...models.LearningFormat import LearningFormat


class CourseFilterSetTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CourseFilterSet
        cls.base_queryset = Course.objects.all()

        user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': user,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        cls.course = Course.objects.create(**{
            'id': 1,
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 1000.0,
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        Course.objects.create(**{
            'id': 2,
            'teacher': teacher,
            'title': 'w' * 50,
            'price': 50.0,
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        course_stat = cls.course.statistic
        course_stat.count_five_rating = 1
        course_stat.save()

    def test_Should_IncludeDefiniteFilters(self):
        expected_filters = [
            'order_by', 'search', 'category_id', 'min_rating', 'max_rating',
            'min_price', 'max_price',
        ]
        real_filters = list(self.tested_class.get_filters())

        self.assertEqual(expected_filters, real_filters)

    def test_Should_SpecificTypeForEachFilter(self):
        expected_filters = {
            'order_by': OrderingFilter,
            'search': CharFilter,
            'category_id': CharFilter,
            'min_rating': NumberFilter,
            'max_rating': NumberFilter,
            'min_price': NumberFilter,
            'max_price': NumberFilter,
        }
        real_filters = {
            key: value.__class__
            for key, value in self.tested_class.get_filters().items()
        }

        self.assertEqual(expected_filters, real_filters)

    def test_When_OrderByCreated_Should_ReturnOrderedData(self):
        data = {
            'order_by': 'created_at',
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.order_by('created_at'))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_OrderByCreatedDesc_Should_ReturnOrderedDescData(self):
        data = {
            'order_by': '-created_at',
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.order_by('-created_at'))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_OrderByPrice_Should_ReturnOrderedData(self):
        data = {
            'order_by': 'price',
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.order_by('price'))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_OrderByPriceDesc_Should_ReturnOrderedDescData(self):
        data = {
            'order_by': '-price',
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.order_by('-price'))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_SearchByTitle_Should_ReturnFilteredDataByTitleIContains(
            self):
        data = {
            'search': 'q',
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'title__icontains': 'q',
        }))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_SearchByTitleWithRandomText_Should_ReturnEmptyQuerySet(self):
        data = {
            'search': 'qw',
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_len = 0
        real_len = len(filtered_data.qs)

        self.assertEqual(expected_len, real_len)

    def test_When_CategoryIdIsNotValid_Should_ReturnGraphQLError(
            self):
        data = {
            #   'OjE==' - ':1'
            'category_id': 'OjE='
        }
        with self.assertRaises(GraphQLError) as _raise:
            self.tested_class(data=data, queryset=self.base_queryset).qs

        expected_raise = 'category_id: This is not global Id.'
        real_raise = str(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_CategoryIdIsValid_Should_ReturnFilteredDataByCategoryId(
            self):
        data = {
            #   'Q2F0ZWdvcnlUeXBlOjE=' - 'CategoryType:1'
            'category_id': 'Q2F0ZWdvcnlUeXBlOjE=',
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'category_id': 1,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_CategoryIdIsNotFound_Should_ReturnNullCourses(
            self):
        data = {
            #   'Q2F0ZWdvcnlUeXBlOjM=' - 'CategoryType:3'
            'category_id': 'Q2F0ZWdvcnlUeXBlOjM='
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'category_id': 3,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_MinRatingUsed_Should_DontUseRatingGreaterThan(self):
        data = {
            'min_rating': 0,
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'statistic__avg_rating__gt': 0,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertNotEqual(expected_queryset, real_queryset)

    def test_When_MinRatingUsed_Should_UseRatingGreaterThanOrEqualWith0(self):
        data = {
            'min_rating': 0,
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'statistic__avg_rating__gte': 0,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_MinRatingUsed_Should_UseRatingGreaterThanOrEqualWith3(self):
        data = {
            'min_rating': 3,
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'statistic__avg_rating__gte': 3,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_MaxRatingUsed_Should_DontUseRatingLessThan(self):
        data = {
            'max_rating': 5,
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'statistic__avg_rating__lt': 5,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertNotEqual(expected_queryset, real_queryset)

    def test_When_MaxRatingUsed_Should_UseRatingLessThanOrEqualWith5(self):
        data = {
            'max_rating': 5,
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'statistic__avg_rating__lte': 5,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_MaxRatingUsed_Should_UseRatingLessThanOrEqualWith3(self):
        data = {
            'max_rating': 3,
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'statistic__avg_rating__lte': 3,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_MinPriceUsed_Should_DontUsePriceGreaterThan(self):
        data = {
            'min_price': 50,
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'price__gt': 50,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertNotEqual(expected_queryset, real_queryset)

    def test_When_MinPriceUsed_Should_DontUsePriceGreaterThanOrEqualWith50(
            self):
        data = {
            'min_price': 50,
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'price__gte': 50,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_MinPriceUsed_Should_DontUsePriceGreaterThanOrEqualWith500(
            self):
        data = {
            'min_price': 500,
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'price__gte': 500,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_MaxPriceUsed_Should_DontUsePriceLessThan(self):
        data = {
            'max_price': 1000,
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'price__lt': 1000,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertNotEqual(expected_queryset, real_queryset)

    def test_When_MaxPriceUsed_Should_UsePriceLessThanOrEqualWith1000(self):
        data = {
            'max_price': 1000,
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'price__lte': 1000,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_MaxPriceUsed_Should_UsePriceLessThanOrEqualWith500(self):
        data = {
            'max_price': 500,
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'price__lte': 500,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)
