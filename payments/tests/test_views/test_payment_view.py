from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.test import APITestCase
from rest_framework.viewsets import ModelViewSet

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF
from users.models import User
from users.models.Teacher import Teacher

from ...filtersets.PaymentFilterBackend import PaymentFilterBackend
from ...models.Payment import Payment
from ...serializers.PaymentSerializer import PaymentSerializer
from ...views.PaymentView import PaymentView


class PaymentViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = PaymentView
        cls.target_database = 'master'
        cls.queryset = Payment.objects.select_related(
            'user', 'course'
        ).filter(is_success=True).all()
        cls.serializer = PaymentSerializer
        cls.url_for_list = reverse('payment_list')

        user = User.objects.create_superuser(**{
            'id': 1,
            'email': 'test@email.com',
            'password': 'password',
        })

        teacher = Teacher.objects.create(**{
            'user': user,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        course = Course.objects.create(**{
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
            'course': course,
            'amount': 100.00,
            'is_success': True,
        })

        client = cls.client_class()
        client.force_authenticate(user=user)
        cls.logged_client = client

    def test_Should_InheritModelViewSet(self):
        expected_super_classes = (
            ModelViewSet,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_QuerySetAsAllUsers(self):
        expected_queryset = self.queryset.query.get_compiler(
            self.target_database,
        ).as_sql()
        real_queryset = self.tested_class.queryset.query.get_compiler(
            self.target_database,
        ).as_sql()

        self.assertEqual(expected_queryset, real_queryset)

    def test_Should_PermissionClassesIsAdminUser(self):
        expected_permission_classes = (
            DjModelPermForDRF,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsQuestionSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_Should_FilterBackendsAsListOfDefinedFilters(self):
        expected_filter_backends = (
            DjangoFilterBackend, PaymentFilterBackend, SearchFilter,
            OrderingFilter,
        )
        real_filter_backends = self.tested_class.filter_backends

        self.assertEqual(expected_filter_backends, real_filter_backends)

    def test_Should_FiltersetFieldsAsListOfDefinedFields(self):
        expected_filterset_fields = (
            'user', 'course',
        )
        real_filterset_fields = self.tested_class.filterset_fields

        self.assertEqual(expected_filterset_fields, real_filterset_fields)

    def test_Should_DefaultOrderingAsId(self):
        expected_fields = (
            '-created_at',
        )
        real_fields = self.tested_class.ordering

        self.assertEqual(expected_fields, real_fields)

    def test_Should_DontOverrideSuperMethods(self):
        expected_methods = [
            ModelViewSet.list,
            ModelViewSet.create,
            ModelViewSet.destroy,
            ModelViewSet.retrieve,
            ModelViewSet.update,
            ModelViewSet.partial_update,
        ]
        real_methods = [
            self.tested_class.list,
            self.tested_class.create,
            self.tested_class.destroy,
            self.tested_class.retrieve,
            self.tested_class.update,
            self.tested_class.partial_update,
        ]

        self.assertEqual(expected_methods, real_methods)

    def test_When_PostMethodForListPayments_Should_ErrorWithStatus405(self):
        response = self.logged_client.post(self.url_for_list, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForListPayments_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForListPayments_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForListPayments_Should_ErrorWithStatus405(self):
        response = self.logged_client.delete(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForListPayments_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url_for_list)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': self.serializer(self.queryset, many=True).data,
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
