import random
from collections import OrderedDict
from itertools import islice

from django.urls import reverse
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.test import APITestCase
from rest_framework.viewsets import ModelViewSet

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF
from users.models import User

from ...models.Resource import Resource
from ...serializers.ResourceSerializer import ResourceSerializer
from ...views.ResourceView import ResourceView


class ResourceViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = ResourceView
        cls.target_database = 'master'
        cls.queryset = Resource.objects.all()
        cls.serializer = ResourceSerializer
        cls.url_for_list = reverse('resources_list')
        cls.url_for_first = reverse('single_resource', kwargs={'pk': 1, })
        cls.url_for_second = reverse('single_resource', kwargs={'pk': 2, })

        cls.user = User.objects.create_superuser(**{
            'id': 1,
            'email': 'test@email.com',
            'password': 'password',
        })

        cls.resource = Resource.objects.create(**{
            'name': 'temporary.jpg',
            'file': 'temporary.jpg',
        })

        cls.data = {
            'name': 'temporary.jpg',
            'file': (
                'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAIAAAACDbGyAAAAAXNSR0IArs4c6'
                'QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAANSURBVB'
                'hXY6AqYGAAAABQAAHTR4hjAAAAAElFTkSuQmCC'
            ),
        }

        client = cls.client_class()
        client.force_authenticate(user=cls.user)
        cls.logged_client = client

    def test_Should_InheritModelViewSet(self):
        expected_super_classes = (
            ModelViewSet,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_QuerySetAsAllResources(self):
        expected_queryset = self.queryset.query.get_compiler(
            self.target_database,
        ).as_sql()
        real_queryset = self.tested_class.queryset.query.get_compiler(
            self.target_database,
        ).as_sql()

        self.assertEqual(expected_queryset, real_queryset)

    def test_Should_PermissionClassesIsAdminUser(self):
        expected_permission_classes = (
            DjModelPermForDRF,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsResourceSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_Should_FilterBackendsAsListOfDefinedFilters(self):
        expected_filter_backends = (
            SearchFilter, OrderingFilter,
        )
        real_filter_backends = self.tested_class.filter_backends

        self.assertEqual(expected_filter_backends, real_filter_backends)

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

    def test_When_PutMethodForListResources_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForListResources_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForListResources_Should_ErrorWithStatus405(self):
        response = self.logged_client.delete(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForListResources_Should_ReturnDataWithStatus200(
            self):
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

        for result in real_data['results']:
            result['file'] = result['file'][17:]

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForListResources_Should_ReturnDataWithStatus201(
            self):
        data = self.data
        response = self.logged_client.post(self.url_for_list, data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = self.serializer(self.queryset.last()).data
        real_data = response.data
        real_data['file'] = real_data['file'][17:]

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForSingleResource_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.post(self.url_for_first, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForSingleResource_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url_for_first)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.resource).data
        real_data = response.data
        real_data['file'] = real_data['file'][17:]

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PutMethodForSingleResource_Should_ReturnDataWithStatus200(
            self):
        data = self.data
        response = self.logged_client.put(self.url_for_first, data)
        self.resource.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.resource).data
        real_data = response.data
        real_data['file'] = real_data['file'][17:]

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PatchMethodForSingleResource_Should_ReturnDataWithStatus200(
            self):
        data = self.data

        ordered_data = OrderedDict(data)
        random_count_attr = random.randint(1, len(ordered_data))
        sliced_data = islice(ordered_data.items(), random_count_attr)
        request_data = OrderedDict(sliced_data)

        response = self.logged_client.patch(self.url_for_first, request_data)
        self.resource.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.resource).data
        real_data = response.data

        if real_data['file']:
            real_data['file'] = real_data['file'][17:]

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_DeleteMethodForSingleResource_Should_ReturnDataWithStatus200(
            self):
        self.logged_client.post(self.url_for_list, data=self.data)

        response = self.logged_client.delete(self.url_for_second)

        expected_status = status.HTTP_204_NO_CONTENT
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)
