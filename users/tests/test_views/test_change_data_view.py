from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import User


class UserChangeDataViewTest(APITestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@email.com',
                                            password='password')

    def test_When_UnauthorizedUser_Should_ErrorWithStatus401(self):
        url = reverse('change')
        response = self.client.post(url)

        expected_status = status.HTTP_401_UNAUTHORIZED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethod_Should_ErrorWithStatus405(self):
        url = reverse('change')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethod_Should_ErrorWithStatus405(self):
        url = reverse('change')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethod_Should_ErrorWithStatus405(self):
        url = reverse('change')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethod_Should_UpdateUserDataAndStatus204(self):
        data = {
            'email': 'test1@email.com',
            'password': 'password1',
            'first_name': 'first_name',
            'last_name': 'last_name'
        }

        url = reverse('change')
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)

        expected_status = status.HTTP_204_NO_CONTENT
        real_status = response.status_code

        excepted_keys = ['email', 'first_name', 'last_name']
        real_keys = list(response.data.keys())

        self.assertEqual(expected_status, real_status)
        self.assertEqual(excepted_keys, real_keys)
