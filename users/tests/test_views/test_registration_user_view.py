from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase

from ...serializers.RegistrationUserSerializer import \
    RegistrationUserSerializer
from ...views.RegistrationUserView import RegistrationUserView


class RegistrationUserViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = RegistrationUserView
        cls.serializer = RegistrationUserSerializer
        cls.url = reverse('signup')

    def test_Should_PermissionClassesIsAllowAny(self):
        expected_permission_classes = (
            AllowAny,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsRegistrationUserSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_When_GetMethodForSingUp_Should_ErrorWithStatus405(self):
        response = self.client.get(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForSingUp_Should_ErrorWithStatus405(self):
        response = self.client.put(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForSingUp_Should_ErrorWithStatus405(self):
        response = self.client.delete(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethodForSingUp_Should_ErrorWithStatus400(self):
        response = self.client.post(self.url, {})
        serializer = self.serializer(data={})
        serializer.is_valid()

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = serializer.errors
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForSingUp_Should_ReturnTokensWithStatus200(self):
        data = {
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'test@email.com',
            'password': 'password',
        }
        response = self.client.post(self.url, data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = {
            'data': 'Confirm your email.',
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
