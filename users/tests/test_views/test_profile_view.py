from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APITestCase

from ...models import User
from ...serializers.ProfileSerializer import ProfileSerializer
from ...views.ProfileView import ProfileView


class ProfileViewTestCase(APITestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = ProfileView
        cls.serializer = ProfileSerializer
        cls.url = reverse('my_profile')

        cls.user = User.objects.create_superuser(**{
            'id': 1,
            'email': 'test@email.com',
            'password': 'password',
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'photo': 'temporary_img',
        })

        cls.data = {
            'first_name': 'w' * 50,
            'last_name': 'w' * 50,
            'photo': (
                'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAIAAAACDbGyAAAAAXNSR0IArs4c6'
                'QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAANSURBVB'
                'hXY6AqYGAAAABQAAHTR4hjAAAAAElFTkSuQmCC'
            ),
        }

        client = cls.client_class()
        client.force_authenticate(user=cls.user)
        cls.logged_client = client

    def test_Should_PermissionClassesIsAdminUser(self):
        expected_permission_classes = (
            IsAuthenticated,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsProfileSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_When_PutMethodForUpdatePassword_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForUpdatePassword_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.delete(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethodForUpdatePassword_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.post(self.url, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForUpdatePassword_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.user).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PatchMethodForUpdatePassword_Should_ReturnDataWithStatus200(
            self):
        data = self.data
        response = self.logged_client.patch(self.url, data)
        self.user.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.user).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
