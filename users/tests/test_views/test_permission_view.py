from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.test import APITestCase
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF
from users.models import User

from ...serializers.PermissionSerializer import PermissionSerializer
from ...views.PermissionView import PermissionView


class PermissionViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = PermissionView
        cls.target_database = 'master'
        cls.queryset = Permission.objects.all()
        cls.serializer = PermissionSerializer
        cls.url_for_list = reverse('permissions_list')
        cls.url_for_single = reverse('single_permission', kwargs={'pk': 1, })

        user = User.objects.create_superuser(**{
            'email': 'test@email.com',
            'password': 'password',
        })

        cls.permission = Permission.objects.get(id=1)

        client = cls.client_class()
        client.force_authenticate(user=user)
        cls.logged_client = client

    def test_Should_InheritModelViewSet(self):
        expected_super_classes = (
            GenericViewSet, ListModelMixin, RetrieveModelMixin,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_QuerySetAsAllPermissions(self):
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

    def test_Should_SerializerClassIsPermissionSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_Should_FilterBackendsAsListOfDefinedFilters(self):
        expected_filter_backends = (
            SearchFilter,
        )
        real_filter_backends = self.tested_class.filter_backends

        self.assertEqual(expected_filter_backends, real_filter_backends)

    def test_Should_DontOverrideSuperMethods(self):
        expected_methods = [
            ModelViewSet.list,
            ModelViewSet.retrieve,
        ]
        real_methods = [
            self.tested_class.list,
            self.tested_class.retrieve,
        ]

        self.assertEqual(expected_methods, real_methods)

    def test_When_PostMethodForListPermissions_Should_ReturnDataWithStatus201(
            self):
        response = self.logged_client.post(self.url_for_list, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForListPermissions_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForListPermissions_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.patch(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForListPermissions_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.delete(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForListPermissions_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url_for_list)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {
            'count': self.queryset.count(),
            'next': 'http://testserver/api/user/permissions/?page=2',
            'previous': None,
            'results': self.serializer(self.queryset[:25], many=True).data,
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForSinglePermission_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.post(self.url_for_single, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForSinglePermission_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.put(self.url_for_single, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForSinglePermiss_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.patch(self.url_for_single, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForSinglePermiss_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.delete(self.url_for_single)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForSinglePermission_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url_for_single)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.permission).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
