from django.test import modify_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer

from ...models import User
from ...views.LogoutUserView import LogoutUserView


@modify_settings(
    MIDDLEWARE={
        'remove': [
            'users.middleware.CookiesMiddleware.CookiesMiddleware',
        ],
    },
)
class LogoutUserViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LogoutUserView
        cls.serializer = TokenBlacklistSerializer
        cls.url = reverse('token_destroy')

        User.objects.create_user(**{
            'email': 'test@email.com',
            'password': 'password',
            'is_active': True,
        })

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

    def test_When_GetMethodForSingOut_Should_ErrorWithStatus405(self):
        response = self.client.get(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForSingOut_Should_ErrorWithStatus405(self):
        response = self.client.put(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForSingOut_Should_ErrorWithStatus405(self):
        response = self.client.patch(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForSingOut_Should_ErrorWithStatus405(self):
        response = self.client.delete(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethodForSingOut_Should_ErrorWithStatus400(self):
        response = self.client.post(self.url, {})

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = {
            'refresh': [
                ErrorDetail(**{
                    'string': 'This field is required.',
                    'code': 'required',
                }),
            ],
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForSingOut_Should_DestroyCookies(self):
        data_login = {
            'email': 'test@email.com',
            'password': 'password',
        }
        url_login = reverse('signin')

        response_login = self.client.post(url_login, data_login)
        refresh_token = response_login.data.get('refresh')

        data = {
            'refresh': refresh_token,
        }
        response = self.client.post(self.url, data)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_cookies = {
            'refresh': {
                'comment': '',
                'domain': '',
                'expires': 'Thu, 01 Jan 1970 00:00:00 GMT',
                'httponly': '',
                'max-age': 0,
                'path': '/api/user/token',
                'samesite': 'strict',
                'secure': '',
                'version': '',
            },
        }
        real_cookies = dict(response.cookies)

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_cookies, real_cookies)
