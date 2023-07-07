import json

from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.test import APITestCase
from rest_framework.viewsets import ModelViewSet

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF
from users.models import User
from users.models.Teacher import Teacher

from ...filtersets.LessonParentFilter import LessonParentFilter
from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...serializers.LessonSerializer import LessonSerializer
from ...serializers.ListLessonSerializer import ListLessonSerializer
from ...views.LessonView import LessonView


class LessonViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LessonView
        cls.target_database = 'master'
        cls.queryset = Lesson.objects.all()
        cls.serializer = LessonSerializer
        cls.url_for_list = reverse('lesson_list')
        cls.url_for_single = reverse('single_lesson', kwargs={'pk': 1, })

        cls.user = User.objects.create_superuser(**{
            'email': 'test@email.com',
            'password': 'password',
        })

        teacher = Teacher.objects.create(**{
            'user': cls.user,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        course = Course.objects.create(**{
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        cls.lesson = Lesson.objects.create(**{
            'course': course,
            'title': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME.value,
            'description': 'q' * 50,
        })

        cls.data = {
            'course': 1,
            'title': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY.value,
            'description': 'q' * 50,
            'body': 'q' * 50,
            'parent': 1,
            'questions': [],
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

    def test_Should_QuerySetAsAllUsers(self):
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

    def test_Should_SerializerClassIsLessonSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_Should_FilterBackendsAsListOfDefinedFilters(self):
        expected_filter_backends = (
            LessonParentFilter, DjangoFilterBackend, SearchFilter,
            OrderingFilter,
        )
        real_filter_backends = self.tested_class.filter_backends

        self.assertEqual(expected_filter_backends, real_filter_backends)

    def test_Should_FiltersetFieldsAsListOfDefinedFields(self):
        expected_filterset_fields = (
            'course', 'parent',
        )
        real_filterset_fields = self.tested_class.filterset_fields

        self.assertEqual(expected_filterset_fields, real_filterset_fields)

    def test_Should_SearchFieldsAsListOfDefinedFields(self):
        expected_search_fields = (
            'title',
        )
        real_search_fields = self.tested_class.search_fields

        self.assertEqual(expected_search_fields, real_search_fields)

    def test_Should_OrderingFieldsAsListOfDefinedFields(self):
        expected_ordering_fields = '__all__'
        real_ordering_fields = self.tested_class.ordering_fields

        self.assertEqual(expected_ordering_fields, real_ordering_fields)

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

    def test_When_PutMethodForListLessons_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForListLessons_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForListLessons_Should_ErrorWithStatus405(self):
        response = self.logged_client.delete(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForListLessons_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url_for_list)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': ListLessonSerializer(self.queryset, many=True).data,
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForListLessons_Should_ReturnDataWithStatus201(
            self):
        data = json.dumps(self.data)
        response = self.logged_client.post(self.url_for_list, data,
                                           content_type='application/json')

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = self.serializer(self.queryset.last()).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForSingleLesson_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.post(self.url_for_single, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForSingleLesson_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url_for_single)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.lesson).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PutMethodForSingleLesson_Should_ReturnDataWithStatus200(
            self):
        data = json.dumps(self.data)
        response = self.logged_client.put(self.url_for_single, data,
                                          content_type='application/json')
        self.lesson.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.lesson).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PatchMethodForSingleLesson_Should_ReturnDataWithStatus200(
            self):
        data = self.data
        del data['questions']
        del data['description']
        request_data = json.dumps(data)

        response = self.logged_client.patch(self.url_for_single, request_data,
                                            content_type='application/json')
        self.lesson.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.lesson).data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_DeleteMethodForSingleLesson_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.delete(self.url_for_single)

        expected_status = status.HTTP_204_NO_CONTENT
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)
