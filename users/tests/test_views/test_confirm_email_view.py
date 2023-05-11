import jwt
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase

from ...models import User
from ...serializers.ConfirmEmailSerializer import ConfirmEmailSerializer
from ...views.ConfirmEmailView import ConfirmEmailView


class UpdatePasswordViewTestCase(APITestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = ConfirmEmailView
        cls.serializer = ConfirmEmailSerializer
        cls.url = reverse('confirm_email')

        cls.user = User.objects.create_superuser(**{
            'id': 1,
            'email': 'test@email.com',
            'password': 'password',
        })

        cls.data = {
            'url': jwt.encode(**{
                'payload': {
                    'user_id': 1,
                },
                'key': settings.SECRET_KEY,
                'algorithm': 'HS256',
            }),
        }

        cls.logged_client = cls.client_class()

    def test_Should_PermissionClassesIsAllowAny(self):
        expected_permission_classes = (
            AllowAny,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsConfirmEmailSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_When_GetMethodForConfirmEmail_Should_ErrorWithStatus405(self):
        response = self.logged_client.get(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForConfirmEmail_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForConfirmEmail_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.patch(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForConfirmEmail_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.delete(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethodForConfirmEmail_Should_ErrorWithStatus400(
            self):
        response = self.logged_client.post(self.url, {})
        serializer = self.serializer(data={})
        serializer.is_valid()

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = serializer.errors
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForConfirmEmail_Should_ReturnDataWithStatus200(
            self):
        data = self.data
        response = self.logged_client.post(self.url, data)
        self.user.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {
            'data': 'Email has been confirmed.',
        }
        real_data = response.data

        expected_email = True
        real_email = self.user.is_active

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
        self.assertEqual(expected_email, real_email)
