from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...filtersets.PaymentFilterBackend import PaymentFilterBackend
from ...models.Payment import Payment


class PaymentFilterBackendTest(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = PaymentFilterBackend
        cls.queryset = Payment.objects.all()

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

        cls.created_at = (timezone.now() - timedelta(days=1)).date()

    def setUp(self):
        self.request = type('request', (object,), {
            'query_params': {
                'created_at': str(self.created_at),
            }
        })

    def test_When_QueryParamsIsEmpty_Should_DontChangeQuerySet(self):
        request = self.request
        request.query_params = {}

        filter_ = self.tested_class()

        expected_data = self.queryset
        real_data = filter_.filter_queryset(request, self.queryset, None)

        self.assertEqual(expected_data, real_data)

    def test_When_QueryParamsWithCreatedAt_Should_FilterQuerySet(self):
        filter_ = self.tested_class()

        expected_data = list(
            self.queryset.filter(created_at__date=self.created_at)
        )
        real_data = list(
            filter_.filter_queryset(self.request, self.queryset, None)
        )

        self.assertEqual(expected_data, real_data)
