from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase

from ...models import User
from ...models.ChangeEmail import ChangeEmail
from ...serializers.ConfirmNewEmailSerializer import ConfirmNewEmailSerializer
from ...views.ConfirmNewEmailView import ConfirmNewEmailView


class UpdatePasswordViewTestCase(APITestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = ConfirmNewEmailView
        cls.serializer = ConfirmNewEmailSerializer
        cls.url = reverse('update_email')

        cls.user = User.objects.create_superuser(**{
            'email': 'test@email.com',
            'password': 'password',
        })

        change_email = ChangeEmail.objects.create(**{
            'user': cls.user,
            'email': 'test1@email.com',
        })

        cls.data = {
            'url': change_email.url,
        }

        cls.logged_client = cls.client_class()

    def test_Should_PermissionClassesIsAdminUser(self):
        expected_permission_classes = (
            AllowAny,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsConfirmNewEmailSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_When_GetMethodForConfirmNewEmail_Should_ErrorWithStatus405(self):
        response = self.logged_client.get(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForConfirmNewEmail_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForConfirmNewEmail_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.patch(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForConfirmNewEmail_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.delete(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethodForConfirmNewEmail_Should_ErrorWithStatus400(
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

    def test_When_PostMethodForConfirmNewEmail_Should_ReturnDataWithStatus200(
            self):
        data = self.data
        response = self.logged_client.post(self.url, data)
        self.user.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {
            'data': 'Email updated.',
        }
        real_data = response.data

        expected_email = 'test1@email.com'
        real_email = self.user.email

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
        self.assertEqual(expected_email, real_email)
