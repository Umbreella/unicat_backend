from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from unicat.rest.views.IntegerChoicesView import IntegerChoiceView
from users.models import User

from ...views.LessonTypeView import LessonTypeView


class LessonTypeViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LessonTypeView
        cls.url_for_list = reverse('lesson_types_list')
        cls.url_for_single = reverse('single_lesson_type',
                                     kwargs={'pk': 1, })

        user = User.objects.create_superuser(**{
            'email': 'test@email.com',
            'password': 'password',
        })

        client = cls.client_class()
        client.force_authenticate(user=user)
        cls.logged_client = client

    def test_Should_InheritIntegerChoiceView(self):
        expected_super_classes = (
            IntegerChoiceView,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_DontOverrideSuperFields(self):
        expected_fields = [
            IntegerChoiceView.queryset,
            IntegerChoiceView.permission_classes,
            IntegerChoiceView.serializer_class,
        ]
        real_fields = [
            self.tested_class.queryset,
            self.tested_class.permission_classes,
            self.tested_class.serializer_class,
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_OverrideSuperFields(self):
        expected_fields = IntegerChoiceView.integer_choices
        real_fields = self.tested_class.integer_choices

        self.assertNotEqual(expected_fields, real_fields)

    def test_When_PostMethodForListLessonTypes_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.post(self.url_for_list, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForListLessonTypes_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.put(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForListLessonTypes_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.patch(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForListLessonTypes_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.delete(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForListLessonTypes_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url_for_list)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {
            'count': 3,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 1,
                    'label': 'Тема',
                },
                {
                    'id': 2,
                    'label': 'Теория',
                },
                {
                    'id': 3,
                    'label': 'Тест',
                },
            ],
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForSingleLessonType_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.post(self.url_for_single, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForSingleLessonType_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.put(self.url_for_single)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForSingleLessonType_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.patch(self.url_for_single)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForSingleLessonType_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.delete(self.url_for_single)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForSingleLessonType_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url_for_single)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {
            'id': 1,
            'label': 'Тема',
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_GetMethodForSingleLessonType_Should_ErrorWithStatus404(
            self):
        url_not_found = reverse('single_lesson_type', kwargs={'pk': 10, })

        response = self.logged_client.get(url_not_found)

        expected_status = status.HTTP_404_NOT_FOUND
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)
