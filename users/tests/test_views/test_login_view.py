from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import User


class UserLoginViewTest(APITestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email='test@email.com', password='password')

    def test_When_GetMethod_Should_ErrorWithStatus405(self):
        url = reverse('signin')
        response = self.client.get(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethod_Should_ErrorWithStatus405(self):
        url = reverse('signin')
        response = self.client.put(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethod_Should_ErrorWithStatus405(self):
        url = reverse('signin')
        response = self.client.patch(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethod_Should_ErrorWithStatus405(self):
        url = reverse('signin')
        response = self.client.delete(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethod_Should_ReturnTokensAndStatus200(self):
        data = {
            'email': 'test@email.com',
            'password': 'password'
        }

        url = reverse('signin')
        response = self.client.post(url, data)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)
