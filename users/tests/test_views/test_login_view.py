from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import User


class UserLoginViewTestCase(APITestCase):
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

        expected_data_keys = ['refresh', 'access']
        real_data_keys = list(response.data.keys())

        tokens_value = response.data.values()
        tokens_is_empty = all([len(token) < 10 for token in tokens_value])

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data_keys, real_data_keys)
        self.assertFalse(tokens_is_empty)

    def test_When_PostMethod_Should_ReturnRefreshTokenInCookies(self):
        data = {
            'email': 'test@email.com',
            'password': 'password'
        }

        url = reverse('signin')
        response = self.client.post(url, data)

        expected_cookies = {
            'refresh': {
                'comment': '',
                'domain': '',
                'expires': '',
                'httponly': True,
                'max-age': '',
                'path': '/api/user/token',
                'samesite': 'strict',
                'secure': True,
                'version': '',
            },
        }
        real_cookies = dict(response.cookies)

        expected_cookies_refresh = response.data['refresh']
        real_cookies_refresh = response.cookies['refresh'].value

        self.assertEqual(expected_cookies, real_cookies)
        self.assertEqual(expected_cookies_refresh, real_cookies_refresh)
