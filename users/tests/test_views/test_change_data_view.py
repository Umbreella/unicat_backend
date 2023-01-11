from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import User
from ...serializers.ChangeDataUserSerializer import ChangeDataUserSerializer


class UserChangeDataViewTestCase(APITestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@email.com',
                                            password='password')

        client = cls.client_class()
        client.force_authenticate(user=cls.user)

        cls.logged_client = client

    def test_When_UnauthorizedUser_Should_ErrorWithStatus401(self):
        url = reverse('change')
        response = self.client.post(url)

        expected_status = status.HTTP_401_UNAUTHORIZED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethod_Should_ErrorWithStatus405(self):
        url = reverse('change')
        response = self.logged_client.get(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethod_Should_ErrorWithStatus405(self):
        url = reverse('change')
        response = self.logged_client.post(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethod_Should_ErrorWithStatus405(self):
        url = reverse('change')
        response = self.logged_client.delete(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodWithFullData_Should_ReturnNewUserDataAndStatus200(
            self):
        data = {
            'email': 'test1@email.com',
            'password': 'password1',
            'first_name': 'first_name',
            'last_name': 'last_name'
        }

        url = reverse('change')
        response = self.logged_client.put(url, data)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        excepted_data = ChangeDataUserSerializer(self.user).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(excepted_data, real_data)

    def test_When_PutMethodWithPartialData_Should_ErrorWithStatus400(self):
        data = {
            'email': 'test1@email.com',
        }

        url = reverse('change')
        response = self.logged_client.put(url, data)

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethod_Should_ReturnNewUserDataAndStatus200(self):
        data = {
            'email': 'test1@email.com',
        }

        url = reverse('change')
        response = self.logged_client.patch(url, data)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        excepted_data = ChangeDataUserSerializer(self.user).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(excepted_data, real_data)
