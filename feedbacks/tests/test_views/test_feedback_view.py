import random
from collections import OrderedDict
from itertools import islice

from django.urls import reverse
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.test import APITestCase
from rest_framework.viewsets import ModelViewSet

from users.models import User

from ...models.Feedback import Feedback
from ...permissions.CreateAnyButEditAdminPermission import \
    CreateAnyButEditAdminPermission
from ...serializers.FeedbackSerializer import FeedbackSerializer
from ...views.FeedbackView import FeedbackView


class FeedbackViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = FeedbackView
        cls.target_database = 'master'
        cls.queryset = Feedback.objects.all()
        cls.serializer = FeedbackSerializer
        cls.url_for_list = reverse('feedbacks_list')
        cls.url_for_single = reverse('single_feedback', kwargs={'pk': 1, })

        user = User.objects.create_superuser(**{
            'email': 'test@email.com',
            'password': 'password',
        })

        cls.feedback = Feedback.objects.create(**{
            'name': 'q' * 50,
            'email': 'q' * 50 + '@admin.com',
            'body': 'q' * 50,
        })

        cls.data = {
            'name': 'w' * 50,
            'email': 'w' * 50 + '@admin.com',
            'body': 'w' * 50,
        }

        client = cls.client_class()
        client.force_authenticate(user=user)
        cls.logged_client = client

    def test_Should_InheritModelViewSet(self):
        expected_super_classes = (
            ModelViewSet,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_QuerySetAsAllEvents(self):
        expected_queryset = self.queryset.query.get_compiler(
            self.target_database,
        ).as_sql()
        real_queryset = self.tested_class.queryset.query.get_compiler(
            self.target_database,
        ).as_sql()

        self.assertEqual(expected_queryset, real_queryset)

    def test_Should_PermissionClassesIsAdminUser(self):
        expected_permission_classes = (
            CreateAnyButEditAdminPermission,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsEventSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_Should_FilterBackendsAsListOfDefinedFilters(self):
        expected_filter_backends = (
            SearchFilter, OrderingFilter,
        )
        real_filter_backends = self.tested_class.filter_backends

        self.assertEqual(expected_filter_backends, real_filter_backends)

    def test_Should_SearchFieldsAsListOfDefinedModelFields(self):
        expected_fields = (
            'email',
        )
        real_fields = self.tested_class.search_fields

        self.assertEqual(expected_fields, real_fields)

    def test_Should_OrderingFieldsAsListOfDefinedModelFields(self):
        expected_fields = (
            'id', 'created_at',
        )
        real_fields = self.tested_class.ordering_fields

        self.assertEqual(expected_fields, real_fields)

    def test_Should_DefaultOrderingAsId(self):
        expected_fields = (
            'id',
        )
        real_fields = self.tested_class.ordering

        self.assertEqual(expected_fields, real_fields)

    def test_Should_DontOverrideSuperMethods(self):
        expected_methods = [
            ModelViewSet.list,
            ModelViewSet.create,
            ModelViewSet.destroy,
            ModelViewSet.retrieve,
            ModelViewSet.update,
            ModelViewSet.partial_update,
        ]
        real_methods = [
            self.tested_class.list,
            self.tested_class.create,
            self.tested_class.destroy,
            self.tested_class.retrieve,
            self.tested_class.update,
            self.tested_class.partial_update,
        ]

        self.assertEqual(expected_methods, real_methods)

    def test_When_PutMethodForListEvents_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForListEvents_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForListEvents_Should_ErrorWithStatus405(self):
        response = self.logged_client.delete(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForListEvents_Should_ReturnDataWithStatus200(self):
        response = self.logged_client.get(self.url_for_list)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': self.serializer(self.queryset, many=True).data,
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForListEvents_Should_ReturnDataWithStatus201(self):
        data = self.data
        response = self.logged_client.post(self.url_for_list, data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = self.serializer(self.queryset.last()).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForSingleEvent_Should_ErrorWithStatus405(self):
        response = self.logged_client.post(self.url_for_single, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForSingleCategory_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url_for_single, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForSingleCategory_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.delete(self.url_for_single)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForSingleEvent_Should_ReturnDataWithStatus200(self):
        response = self.logged_client.get(self.url_for_single)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.feedback).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PatchMethodForSingleCategory_Should_ReturnDataWithStatus200(
            self):
        data = self.data

        ordered_data = OrderedDict(data)
        random_count_attr = random.randint(1, len(ordered_data))
        sliced_data = islice(ordered_data.items(), random_count_attr)
        request_data = OrderedDict(sliced_data)

        response = self.logged_client.patch(self.url_for_single, request_data)
        self.feedback.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.feedback).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
