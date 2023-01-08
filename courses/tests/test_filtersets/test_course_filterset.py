from django.test import TestCase

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
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 500.0,
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
            'description': 'q' * 50,
        })

        Course.objects.create(**{
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
            'description': 'q' * 50,
        })

    def test_Should_IncludeDefiniteFilters(self):
        dict_keys = dict(self.tested_class.get_filters()).keys()

        expected_filters = [
            'order_by', 'search', 'category',
        ]
        real_filters = [key for key in dict_keys]

        self.assertEqual(expected_filters, real_filters)

    def test_When_OrderByCreated_Should_ReturnOrderedData(self):
        data = {
            'order_by': 'created_at',
        }
        base_queryset = Course.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = list(base_queryset.order_by('created_at'))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_OrderByCreatedDesc_Should_ReturnOrderedDescData(self):
        data = {
            'order_by': '-created_at',
        }
        base_queryset = Course.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = list(base_queryset.order_by('-created_at'))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_OrderByPrice_Should_ReturnOrderedData(self):
        data = {
            'order_by': 'price',
        }
        base_queryset = Course.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = list(base_queryset.order_by('price'))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_OrderByPriceDesc_Should_ReturnOrderedDescData(self):
        data = {
            'order_by': '-price',
        }
        base_queryset = Course.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = list(base_queryset.order_by('-price'))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_SearchByTitle_Should_ReturnFilteredDataByTitleIContains(
            self):
        data = {
            'search': 'q',
        }
        base_queryset = Course.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = self.course
        real_queryset = filtered_data.qs.first()

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_SearchByTitleWithRandomText_Should_ReturnNullCourse(self):
        data = {
            'search': 'qw',
        }
        base_queryset = Course.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = None
        real_queryset = filtered_data.qs.first()

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_CategoryIdIsValid_Should_ReturnFilteredDataByCategoryId(
            self):
        data = {
            #   'OjE=' - ':1'
            'category': 'OjE=',
        }
        base_queryset = Course.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = self.course
        real_queryset = filtered_data.qs.first()

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_CategoryIdIsNotValid_Should_ReturnNullCourses(
            self):
        data = {
            #   'OjM=' - ':3'
            'category': 'OjM=',
        }
        base_queryset = Course.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = None
        real_queryset = filtered_data.qs.first()

        self.assertEqual(expected_queryset, real_queryset)
