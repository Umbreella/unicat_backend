from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django_filters import OrderingFilter

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...filtersets.PaymentFilterSet import PaymentFilterSet
from ...models.Payment import Payment


class PaymentFilterSetTest(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = PaymentFilterSet

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

        first_course = Course.objects.create(**{
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        second_course = Course.objects.create(**{
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        third_course = Course.objects.create(**{
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        Payment.objects.create(**{
            'id': 'q' * 27,
            'user': user,
            'course': first_course,
            'amount': 100.0,
            'created_at': timezone.now() - timedelta(days=3),
            'is_success': True,
        })

        Payment.objects.create(**{
            'id': 'w' * 27,
            'user': user,
            'course': second_course,
            'amount': 100.0,
            'created_at': timezone.now() - timedelta(days=1),
            'is_success': True,
        })

        Payment.objects.create(**{
            'id': 'e' * 27,
            'user': user,
            'course': third_course,
            'amount': 100.0,
            'created_at': timezone.now() - timedelta(days=2),
            'is_success': True,
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
            'order_by': 'created_at',
        }
        base_queryset = Payment.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = list(base_queryset.order_by('created_at'))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_OrderByTitleDesc_Should_ReturnOrderedDescData(self):
        data = {
            'order_by': '-created_at',
        }
        base_queryset = Payment.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = list(base_queryset.order_by('-created_at'))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)
