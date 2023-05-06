from django.urls import reverse
from django_weasyprint import WeasyTemplateResponseMixin
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.test import APITestCase

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.LearningFormat import LearningFormat
from ...models.UserCourse import UserCourse
from ...views.UserCertificateView import UserCertificateView


class UserCertificateViewTestCase(APITestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserCertificateView
        cls.url_on_first_course = reverse(**{
            'viewname': 'user_certificate',
            'kwargs': {
                'course_id': 'Q291cnNlVHlwZTox',
            },
        })
        cls.url_on_second_course = reverse(**{
            'viewname': 'user_certificate',
            'kwargs': {
                'course_id': 'Q291cnNlVHlwZToy',
            },
        })

        user = User.objects.create_superuser(**{
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
            'discount': None,
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
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        UserCourse.objects.create(**{
            'course': first_course,
            'user': user,
            'count_lectures_completed': 50,
            'count_independents_completed': 50,
        })

        UserCourse.objects.create(**{
            'course': second_course,
            'user': user,
        })

        client = cls.client_class()
        client.force_authenticate(user=user)
        cls.logged_client = client

    def test_Should_InheritListApiViewAndWeasyTemplate(self):
        expected_super_classes = (
            ListAPIView, WeasyTemplateResponseMixin,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_PermissionClassesIsAdminUser(self):
        expected_permission_classes = (
            IsAuthenticated,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsBaseSerializer(self):
        expected_serializer_class = Serializer
        real_serializer_class = self.tested_class.serializer_class

        self.assertEqual(expected_serializer_class, real_serializer_class)

    def test_When_PostMethodForSingleCertificate_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.post(self.url_on_first_course, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForSingleCertificate_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.put(self.url_on_first_course)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForSingleCertificate_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.patch(self.url_on_first_course)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForSingleCertificate_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.delete(self.url_on_first_course)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForCreatedCertificate_Should_ReturnFile(self):
        response = self.logged_client.get(self.url_on_first_course)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_content_type = 'application/pdf'
        real_content_type = response.headers.get('Content-Type')

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_content_type, real_content_type)

    def test_When_GetMethodForEmptyCertificate_Should_ErrorNotHaveCertificate(
            self):
        response = self.logged_client.get(self.url_on_second_course)

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = {
            'course_id': [
                'You do not have a course certificate.',
            ],
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
