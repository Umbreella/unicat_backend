from django.urls import reverse
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.test import APITestCase
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.CourseBody import CourseBody
from ...models.LearningFormat import LearningFormat
from ...serializers.CourseSerializer import CourseSerializer
from ...serializers.ListCourseSerializer import ListCourseSerializer
from ...views.CourseView import CourseView


class CourseViewTestCase(APITestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CourseView
        cls.target_database = 'master'
        cls.queryset = Course.objects.all()
        cls.serializer = CourseSerializer
        cls.url_for_list = reverse('course_list')
        cls.url_for_single = reverse('single_course', kwargs={'pk': 1, })

        first_user = User.objects.create_superuser(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        second_user = User.objects.create_user(**{
            'email': 'w' * 50 + '@q.qq',
            'password': 'w' * 50,
        })

        first_teacher = Teacher.objects.create(**{
            'user': first_user,
            'description': 'q' * 50,
        })

        Teacher.objects.create(**{
            'user': second_user,
            'description': 'q' * 50,
        })

        first_category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        Category.objects.create(**{
            'title': 'w' * 50,
        })

        cls.course = Course.objects.create(**{
            'teacher': first_teacher,
            'title': 'q' * 50,
            'price': 50.0,
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': first_category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        CourseBody.objects.create(**{
            'course': cls.course,
            'body': 'q' * 50,
        })

        cls.data = {
            'teacher': 1,
            'title': 'q' * 50,
            'price': 50.0,
            'discount': 'null',
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': 1,
            'category': 1,
            'short_description': 'q' * 50,
            'body': 'w' * 50,
            'preview': (
                'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAIAAAACDbGyAAAAAXNSR0IArs4c6'
                'QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAANSURBVB'
                'hXY6AqYGAAAABQAAHTR4hjAAAAAElFTkSuQmCC'
            ),
        }

        client = cls.client_class()
        client.force_authenticate(user=first_user)
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
            IsAdminUser,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsCommentSerializer(self):
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

    def test_Should_OrderingFieldsAsListOfDefinedModelFields(self):
        expected_fields = '__all__'
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

    def test_Should_OverrideSuperMethods(self):
        expected_methods = [
            ModelViewSet.list,
        ]
        real_methods = [
            self.tested_class.list,
        ]

        self.assertNotEqual(expected_methods, real_methods)

    def test_When_PutMethodForListCourses_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForListCourses_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForListCourses_Should_ErrorWithStatus405(
            self):
        response = self.logged_client.delete(self.url_for_list)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForListCourses_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url_for_list)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': ListCourseSerializer(self.queryset, many=True).data,
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForListCourses_Should_ReturnDataWithStatus201(
            self):
        data = self.data
        response = self.logged_client.post(self.url_for_list, data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = self.serializer(self.queryset.last()).data
        real_data = response.data
        real_data['preview'] = real_data['preview'][17:]

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodForSingleCourse_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.post(self.url_for_single, {})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethodForSingleCourse_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.get(self.url_for_single)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.course).data
        real_data = response.data
        real_data['preview'] = real_data['preview'][17:]

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PutMethodForSingleCourse_Should_ReturnDataWithStatus200(
            self):
        data = self.data
        response = self.logged_client.put(self.url_for_single, data)
        self.course.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.course).data
        real_data = response.data

        expected_data.pop('preview')
        expected_preview = 'temporary_img'
        real_preview = real_data.pop('preview').split('/')[-1]

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
        self.assertNotEqual(expected_preview, real_preview)

    def test_When_PatchMethodForSingleCourse_Should_ReturnDataWithStatus200(
            self):
        data = self.data
        response = self.logged_client.patch(self.url_for_single, data)
        self.course.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = self.serializer(self.course).data
        real_data = response.data

        expected_data.pop('preview')
        expected_preview = 'temporary_img'
        real_preview = real_data.pop('preview').split('/')[-1]

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
        self.assertNotEqual(expected_preview, real_preview)

    def test_When_DeleteMethodForSingleCourse_Should_ReturnDataWithStatus200(
            self):
        response = self.logged_client.delete(self.url_for_single)

        expected_status = status.HTTP_204_NO_CONTENT
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)
