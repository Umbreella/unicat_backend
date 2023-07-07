from django.test import TestCase
from django_filters import BooleanFilter, CharFilter
from graphql import GraphQLError

from users.models import User
from users.models.Teacher import Teacher

from ...filtersets.UserCourseFilterSet import UserCourseFilterSet
from ...models.Category import Category
from ...models.Course import Course
from ...models.LearningFormat import LearningFormat


class UserCourseFilterSetTest(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserCourseFilterSet
        cls.base_queryset = Course.objects.all()

        cls.user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': cls.user,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        cls.first_course = Course.objects.create(**{
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 1000.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        cls.second_course = Course.objects.create(**{
            'teacher': teacher,
            'title': 'w' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        cls.first_course.listeners.add(cls.user)
        cls.second_course.listeners.add(cls.user)

        user_course = cls.user.my_progress.get(course=cls.first_course)
        user_course.count_lectures_completed = 50
        user_course.count_independents_completed = 50
        user_course.save()

    def test_Should_IncludeDefiniteFilters(self):
        expected_filters = [
            'order_by', 'search', 'is_completed',
        ]
        real_filters = list(self.tested_class.get_filters())

        self.assertEqual(expected_filters, real_filters)

    def test_Should_SpecificTypeForEachFilter(self):
        expected_filters = {
            'order_by': CharFilter,
            'search': CharFilter,
            'is_completed': BooleanFilter,
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

        expected_queryset = list(self.base_queryset.order_by(
            'user_courses__created_at',
        ))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_OrderByCreatedDesc_Should_ReturnOrderedDescData(self):
        data = {
            'order_by': '-created_at',
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.order_by(
            '-user_courses__created_at',
        ))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_OrderByLastView_Should_ReturnOrderedData(self):
        data = {
            'order_by': 'last_view',
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.order_by(
            'user_courses__last_view',
        ))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_OrderByLastViewDesc_Should_ReturnOrderedDescData(self):
        data = {
            'order_by': '-last_view',
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.order_by(
            '-user_courses__last_view',
        ))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_OrderByNotValid_Should_ReturnGraphQLError(self):
        data = {
            'order_by': 'qwer',
        }
        with self.assertRaises(GraphQLError) as _raise:
            self.tested_class(data=data, queryset=self.base_queryset).qs

        expected_raise = 'Not valid choices for orderBy.'
        real_raise = str(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

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

    def test_When_IsCompletedTrue_Should_ReturnCourseIfUserCourseComplete(
            self):
        data = {
            'is_completed': True,
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'user_courses__completed_at__isnull': False,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_IsCompletedFalse_Should_ReturnCourseIfUserCourseNotComplete(
            self):
        data = {
            'is_completed': False,
        }
        filtered_data = self.tested_class(data=data,
                                          queryset=self.base_queryset)

        expected_queryset = list(self.base_queryset.filter(**{
            'user_courses__completed_at__isnull': True,
        }))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)
