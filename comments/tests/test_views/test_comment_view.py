from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.test import APITestCase
from rest_framework.viewsets import ModelViewSet

from events.models.New import New
from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF
from users.models import User

from ...models.Comment import Comment
from ...models.CommentedTypeChoices import CommentedTypeChoices
from ...serializers.CommentSerializer import CommentSerializer
from ...views.CommentView import CommentView


class CommentViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CommentView
        cls.target_database = 'master'
        cls.queryset = Comment.objects.all()
        cls.serializer = CommentSerializer
        cls.url_for_list = reverse('comments')
        cls.url_for_single = reverse('single_comment', kwargs={'pk': 1, })

        user = User.objects.create_superuser(**{
            'email': 'test@email.com',
            'password': 'password',
        })

        New.objects.create(**{
            'preview': 'temporary_img',
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'author': user,
        })

        cls.comment = Comment.objects.create(**{
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedTypeChoices.NEWS,
            'commented_id': 1,
        })

        client = cls.client_class()
        client.force_authenticate(user=user)
        cls.logged_client = client

    def test_Should_InheritModelViewSet(self):
        expected_super_classes = (
            ModelViewSet,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_QuerySetAsAllComments(self):
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

    def test_Should_SerializerClassIsCommentSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_Should_FilterBackendsAsListOfDefinedFilters(self):
        expected_filter_backends = (
            DjangoFilterBackend, OrderingFilter,
        )
        real_filter_backends = self.tested_class.filter_backends

        self.assertEqual(expected_filter_backends, real_filter_backends)

    def test_Should_FilterSetFieldsAsListOfDefinedModelFields(self):
        expected_filterset_fields = (
            'commented_type',
        )
        real_filterset_fields = self.tested_class.filterset_fields

        self.assertEqual(expected_filterset_fields, real_filterset_fields)

    def test_Should_DefaultOrderingAsDescId(self):
        expected_ordering = (
            '-id',
        )
        real_ordering = self.tested_class.ordering

        self.assertEqual(expected_ordering, real_ordering)

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

    def test_When_PostMethodForListComments_Should_ErrorWithStatus405(self):
        response = self.logged_client.post(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForListComments_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForListComments_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForListComments_Should_ErrorWithStatus405(self):
        response = self.logged_client.delete(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForListComments_Should_ReturnDataWithStatus200(
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

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForSingleComment_Should_ErrorWithStatus405(self):
        response = self.logged_client.post(self.url_for_single)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForSingleComment_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url_for_single)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForSingleComment_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.url_for_single)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForSingleComment_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url_for_single)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.comment).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_DeleteMethodForSingleComment_Should_DeleteDataWithStatus204(
            self):
        response = self.logged_client.delete(self.url_for_single)

        expected_status = status.HTTP_204_NO_CONTENT
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)
