from datetime import timedelta

from django.db import connections
from django.urls import reverse
from django.utils import timezone
from django.utils.connection import ConnectionProxy
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APITestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.Discount import Discount
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Payment import Payment
from ...serializers.PaymentCourseSerializer import PaymentCourseSerializer
from ...views.PaymentCreateView import PaymentCreateView


class PaymentCreateViewTestCase(APITestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = PaymentCreateView
        cls.serializer = PaymentCourseSerializer
        cls.url = reverse('payment_create')

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

        Course.objects.create(**{
            'id': 1,
            'teacher': teacher,
            'title': 'q' * 50,
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

        with ConnectionProxy(connections, 'master').cursor() as c:
            c.execute("""
            INSERT INTO courses_discount(
                percent,
                start_date,
                end_date,
                course_id
            )
            VALUES (10, '%s', '%s', 1);
            """ % (
                timezone.now() - timedelta(days=5),
                timezone.now() + timedelta(days=5),
            ))

        cls.data = {
            'course_id': 'Q291cnNlVHlwZTox',
        }

        client = cls.client_class()
        client.force_authenticate(user=user)
        cls.logged_client = client

        cls.date_format = '%H-%M %d-%m-%Y'

    def test_Should_PermissionClassesIsAuthenticated(self):
        expected_permission_classes = (
            IsAuthenticated,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsLessonSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_When_GetMethodForPaymentCreate_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.get(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForPaymentCreate_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.put(self.url, data={})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForPaymentCreate_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.patch(self.url, data={})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForPaymentCreate_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.delete(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethodForPaymentCreate_Should_ErrorDataWithStatus400(
            self):
        response = self.logged_client.post(self.url, data={})
        serializer = self.serializer(data={})
        serializer.is_valid()

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = serializer.errors
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodWithActiveDiscount_Should_ReturnDataWithStatus201(
            self):
        data = self.data
        response = self.logged_client.post(self.url, data=data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = {
            'amount': 4500,
            'clientSecret': (
                'pi_1Mxd0wLKkAKty0Q87fIqvZs9_secret_LMr7KUxVEmZu8YXAp0RUuhsic'
            ),
        }
        real_data = response.data

        expected_count_payment = 1
        real_count_payment = len(Payment.objects.all())

        expected_dict = {
            'user_id': 1,
            'course_id': 1,
            'amount': 45.00,
            'is_success': False,
        }
        real_dict = dict(Payment.objects.last())

        expected_id = ''
        real_id = real_dict.pop('id')

        expected_created = timezone.now().strftime(self.date_format)
        real_created = real_dict.pop('created_at').strftime(self.date_format)

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
        self.assertEqual(expected_count_payment, real_count_payment)
        self.assertEqual(expected_dict, real_dict)
        self.assertNotEqual(expected_id, real_id)
        self.assertEqual(expected_created, real_created)

    def test_When_PostMethodWithOutDiscount_Should_ReturnDataWithStatus201(
            self):
        Discount.objects.all().delete()

        data = self.data
        response = self.logged_client.post(self.url, data=data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = {
            'amount': 5000,
            'clientSecret': (
                'pi_1Mxd0wLKkAKty0Q87fIqvZs9_secret_LMr7KUxVEmZu8YXAp0RUuhsic'
            ),
        }
        real_data = response.data

        expected_count_payment = 1
        real_count_payment = len(Payment.objects.all())

        expected_dict = {
            'user_id': 1,
            'course_id': 1,
            'amount': 50.00,
            'is_success': False,
        }
        real_dict = dict(Payment.objects.last())

        expected_id = ''
        real_id = real_dict.pop('id')

        expected_created = timezone.now().strftime(self.date_format)
        real_created = real_dict.pop('created_at').strftime(self.date_format)

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
        self.assertEqual(expected_count_payment, real_count_payment)
        self.assertEqual(expected_dict, real_dict)
        self.assertNotEqual(expected_id, real_id)
        self.assertEqual(expected_created, real_created)
