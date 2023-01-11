from django.test import modify_settings
from django.urls import path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from users.models import User

from ...views.CommentView import CommentView


@modify_settings(
    MIDDLEWARE={
        'remove': [
            'users.middleware.CookiesMiddleware.CookiesMiddleware',
        ],
    }
)
class CommentViewTest(APITestCase, URLPatternsTestCase):
    databases = {'master'}

    urlpatterns = [
        path('', CommentView.as_view(), name='comments'),
    ]

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CommentView

        user = User.objects.create_user(email='test@email.com',
                                        password='password')

        client = cls.client_class()
        client.force_authenticate(user=user)

        cls.logged_client = client

    def test_Should_PermissionClassesIsAuthenticated(self):
        perm_classes = self.tested_class.permission_classes

        expected_classes = [
            'IsAuthenticated',
        ]
        real_classes = [_class.__name__ for _class in perm_classes]

        self.assertEqual(expected_classes, real_classes)

    def test_When_GetMethod_Should_ErrorWithStatus405(self):
        url = reverse('comments')
        response = self.logged_client.get(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethod_Should_ErrorWithStatus405(self):
        url = reverse('comments')
        response = self.logged_client.put(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethod_Should_ErrorWithStatus405(self):
        url = reverse('comments')
        response = self.logged_client.patch(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethod_Should_ErrorWithStatus405(self):
        url = reverse('comments')
        response = self.logged_client.delete(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethod_Should_TypeError(self):
        url = reverse('comments')

        with self.assertRaises(TypeError) as _raise:
            self.logged_client.post(url)

        expected_raise = "'NoneType' object is not callable"
        real_raise = str(_raise.exception)

        self.assertEqual(expected_raise, real_raise)
