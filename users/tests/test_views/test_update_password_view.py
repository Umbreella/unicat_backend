from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase

from ...models import User
from ...models.ResetPassword import ResetPassword
from ...serializers.UpdatePasswordSerializer import UpdatePasswordSerializer
from ...views.UpdatePasswordView import UpdatePasswordView


class UpdatePasswordViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UpdatePasswordView
        cls.serializer = UpdatePasswordSerializer
        cls.url = reverse('password_update')

        cls.user = User.objects.create_superuser(**{
            'id': 1,
            'email': 'test@email.com',
            'password': 'password',
        })

        reset_password = ResetPassword.objects.create(**{
            'user': cls.user,
        })

        cls.data = {
            'url': reset_password.url,
            'password': 'password1',
        }

        cls.logged_client = cls.client_class()

    def test_Should_PermissionClassesIsAllowAny(self):
        expected_permission_classes = (
            AllowAny,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsUpdatePasswordSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_When_GetMethodForUpdatePassword_Should_ErrorWithStatus405(self):
        response = self.logged_client.get(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForUpdatePassword_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForUpdatePassword_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForUpdatePassword_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.delete(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethodForUpdatePassword_Should_ErrorWithStatus400(self):
        response = self.logged_client.post(self.url, {})
        serializer = self.serializer(data={})
        serializer.is_valid()

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = serializer.errors
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForUpdatePassword_Should_ReturnDataWithStatus200(
            self):
        data = self.data
        response = self.logged_client.post(self.url, data)
        self.user.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {
            'data': 'Password updated.',
        }
        real_data = response.data

        prev_password = self.user.check_password('password')
        new_password = self.user.check_password('password1')

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
        self.assertNotEqual(prev_password, new_password)
