import random
from collections import OrderedDict
from itertools import islice

from django.urls import reverse
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.test import APITestCase
from rest_framework.viewsets import ModelViewSet

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF
from users.models import User

from ...models.Teacher import Teacher
from ...serializers.ListTeacherSerializer import ListTeacherSerializer
from ...serializers.TeacherSerializer import TeacherSerializer
from ...views.TeacherView import TeacherView


class TeacherViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = TeacherView
        cls.target_database = 'master'
        cls.queryset = Teacher.objects.select_related('user').all()
        cls.serializer = TeacherSerializer
        cls.url_for_list = reverse('teacher_list')
        cls.url_for_single = reverse('single_teacher', kwargs={'pk': 1, })

        user = User.objects.create_superuser(**{
            'id': 1,
            'email': 'test@email.com',
            'password': 'password',
        })

        User.objects.create_user(**{
            'id': 2,
            'email': 'test1@email.com',
            'password': 'password',
        })

        cls.teacher = Teacher.objects.create(**{
            'user': user,
            'description': 'q' * 50,
        })

        cls.data = {
            'user': 2,
            'description': 'q' * 50,
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

    def test_Should_QuerySetAsAllTeachers(self):
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

    def test_Should_SerializerClassIsTeacherSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_Should_FilterBackendsAsListOfDefinedFilters(self):
        expected_filter_backends = (
            OrderingFilter,
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
            ModelViewSet.create,
            ModelViewSet.destroy,
            ModelViewSet.retrieve,
            ModelViewSet.update,
            ModelViewSet.partial_update,
        ]
        real_methods = [
            self.tested_class.create,
            self.tested_class.destroy,
            self.tested_class.retrieve,
            self.tested_class.update,
            self.tested_class.partial_update,
        ]

        self.assertEqual(expected_methods, real_methods)

    def test_Should_OverrideSuperMethodList(self):
        expected_method = ModelViewSet.list
        real_method = self.tested_class.list

        self.assertNotEqual(expected_method, real_method)

    def test_When_PutMethodForListTeachers_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForListTeachers_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForListTeachers_Should_ErrorWithStatus405(self):
        response = self.logged_client.delete(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForListTeachers_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url_for_list)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': ListTeacherSerializer(self.queryset, many=True).data,
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForListTeachers_Should_ReturnDataWithStatus201(
            self):
        data = self.data
        response = self.logged_client.post(self.url_for_list, data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = self.serializer(self.queryset.last()).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForSingleTeacher_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.post(self.url_for_single, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForSingleTeacher_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url_for_single)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.teacher).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PutMethodForSingleTeacher_Should_ReturnDataWithStatus200(
            self):
        data = self.data
        response = self.logged_client.put(self.url_for_single, data)
        self.teacher.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.teacher).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PatchMethodForSingleTeacher_Should_ReturnDataWithStatus200(
            self):
        data = self.data

        ordered_data = OrderedDict(data)
        random_count_attr = random.randint(1, len(ordered_data))
        sliced_data = islice(ordered_data.items(), random_count_attr)
        request_data = OrderedDict(sliced_data)

        response = self.logged_client.patch(self.url_for_single, request_data)
        self.teacher.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.teacher).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_DeleteMethodForSingleTeacher_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.delete(self.url_for_single)

        expected_status = status.HTTP_204_NO_CONTENT
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)
