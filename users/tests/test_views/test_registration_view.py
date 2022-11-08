from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserRegistrationViewTest(APITestCase):
    databases = {'master'}

    def test_When_GetMethod_Should_ErrorWithStatus405(self):
        url = reverse('signup')
        response = self.client.get(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethod_Should_ErrorWithStatus405(self):
        url = reverse('signup')
        response = self.client.put(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethod_Should_ErrorWithStatus405(self):
        url = reverse('signup')
        response = self.client.delete(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethod_Should_ReturnTokensAndStatus200(self):
        data = {
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'test@email.com',
            'password': 'password'
        }

        url = reverse('signup')
        response = self.client.post(url, data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)
