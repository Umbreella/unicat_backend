from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase

from ...models import User
from ...serializers.ResetPasswordSerializer import ResetPasswordSerializer
from ...views.ResetPasswordView import ResetPasswordView


class UpdatePasswordViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = ResetPasswordView
        cls.serializer = ResetPasswordSerializer
        cls.url = reverse('password_reset')

        cls.user = User.objects.create_superuser(**{
            'id': 1,
            'email': 'test@email.com',
            'password': 'password',
        })

        cls.data = {
            'email': 'test@email.com',
        }

        cls.logged_client = cls.client_class()

    def test_Should_PermissionClassesIsAdminUser(self):
        expected_permission_classes = (
            AllowAny,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsResetPasswordSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_When_GetMethodForResetPassword_Should_ErrorWithStatus405(self):
        response = self.logged_client.get(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForResetPassword_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForResetPassword_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForResetPassword_Should_ErrorWithStatus405(self):
        response = self.logged_client.delete(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethodForResetPassword_Should_ErrorWithStatus400(self):
        response = self.logged_client.post(self.url, {})
        serializer = self.serializer(data={})
        serializer.is_valid()

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = serializer.errors
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForResetPassword_Should_ReturnDataWithStatus201(
            self):
        data = self.data
        response = self.logged_client.post(self.url, data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = {
            'data': 'Email sent.',
        }
        real_data = response.data

        expected_len_mails = 1
        real_len_mails = len(mail.outbox)

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
        self.assertEqual(expected_len_mails, real_len_mails)
