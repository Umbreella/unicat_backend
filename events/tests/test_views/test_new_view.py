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

from ...models.New import New
from ...serializers.ListNewSerializer import ListNewSerializer
from ...serializers.NewSerializer import NewSerializer
from ...views.NewView import NewView


class NewViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = NewView
        cls.target_database = 'master'
        cls.queryset = New.objects.all()
        cls.serializer = NewSerializer
        cls.url_for_list = reverse('news_list')
        cls.url_for_single = reverse('single_new', kwargs={'pk': 1, })

        user = User.objects.create_superuser(**{
            'email': 'test@email.com',
            'password': 'password',
        })

        cls.new = New.objects.create(**{
            'preview': 'temporary_img',
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'author': user,
        })

        cls.data = {
            'title': 'w' * 50,
            'short_description': 'w' * 50,
            'description': 'w' * 50,
            'author': 1,
            'preview': (
                'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAIAAAACDbGyAAAAAXNSR0IArs4c6'
                'QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAANSURBVB'
                'hXY6AqYGAAAABQAAHTR4hjAAAAAElFTkSuQmCC'
            ),
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

    def test_Should_QuerySetAsAllNews(self):
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

    def test_Should_SerializerClassIsNewSerializer(self):
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
            'title',
        )
        real_fields = self.tested_class.search_fields

        self.assertEqual(expected_fields, real_fields)

    def test_Should_DefaultOrderingAsId(self):
        expected_fields = (
            'id',
        )
        real_fields = self.tested_class.ordering

        self.assertEqual(expected_fields, real_fields)

    def test_Should_DontOverrideSuperMethods(self):
        expected_methods = [
            ModelViewSet.destroy,
            ModelViewSet.retrieve,
            ModelViewSet.update,
            ModelViewSet.partial_update,
        ]
        real_methods = [
            self.tested_class.destroy,
            self.tested_class.retrieve,
            self.tested_class.update,
            self.tested_class.partial_update,
        ]

        self.assertEqual(expected_methods, real_methods)

    def test_Should_OverrideSuperMethodCreate(self):
        expected_method = ModelViewSet.create
        real_method = self.tested_class.create

        self.assertNotEqual(expected_method, real_method)

    def test_Should_OverrideSuperMethodList(self):
        expected_method = ModelViewSet.list
        real_method = self.tested_class.list

        self.assertNotEqual(expected_method, real_method)

    def test_When_PutMethodForListNews_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForListNews_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForListNews_Should_ErrorWithStatus405(self):
        response = self.logged_client.delete(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForListNews_Should_ReturnDataWithStatus200(self):
        response = self.logged_client.get(self.url_for_list)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': ListNewSerializer(self.queryset, many=True).data,
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForListNews_Should_ReturnDataWithStatus201(self):
        data = self.data
        response = self.logged_client.post(self.url_for_list, data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = self.serializer(self.queryset.last()).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForSingleNew_Should_ReturnDataWithStatus200(self):
        response = self.logged_client.post(self.url_for_single, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForSingleNew_Should_ReturnDataWithStatus200(self):
        response = self.logged_client.get(self.url_for_single)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.new).data
        real_data = response.data
        real_data['preview'] = real_data['preview'][17:]

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PutMethodForSingleNew_Should_ReturnDataWithStatus200(self):
        data = self.data
        response = self.logged_client.put(self.url_for_single, data)
        self.new.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.new).data
        real_data = response.data
        real_data['preview'] = real_data['preview'][17:]

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PatchMethodForSingleNew_Should_ReturnDataWithStatus200(self):
        data = self.data

        ordered_data = OrderedDict(data)
        random_count_attr = random.randint(1, len(ordered_data))
        sliced_data = islice(ordered_data.items(), random_count_attr)
        request_data = OrderedDict(sliced_data)

        response = self.logged_client.patch(self.url_for_single, request_data)
        self.new.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.new).data
        real_data = response.data
        real_data['preview'] = real_data['preview'][17:]

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_DeleteMethodForSingleNew_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.delete(self.url_for_single)

        expected_status = status.HTTP_204_NO_CONTENT
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)
