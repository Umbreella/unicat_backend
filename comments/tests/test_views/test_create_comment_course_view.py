from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Comment import Comment
from ...serializers.CreateCommentCourseSerializer import \
    CreateCommentCourseSerializer
from ...views.CreateCommentCourseView import CreateCommentCourseView
from ...views.CreateCommentView import CreateCommentView


class CreateCommentCourseViewTestCase(APITestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CreateCommentCourseView
        cls.serializer_class = CreateCommentCourseSerializer
        cls.url = reverse('create_comment_course')

        user = User.objects.create_user(email='test@email.com',
                                        password='password')

        teacher = Teacher.objects.create(**{
            'user': user,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        Course.objects.create(**{
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 50.0,
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        client = cls.client_class()
        client.force_authenticate(user=user)
        cls.logged_client = client

    def test_Should_SuperClassIsCommentView(self):
        expected_super_classes = (
            CreateCommentView,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_SerializerClassIsCommentCourseSerializer(self):
        expected_serializer = self.serializer_class
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_Should_DontOverridePermission(self):
        expected_permission_classes = CreateCommentView.permission_classes
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_DontOverridePostMethod(self):
        expected_method = CreateCommentView.post
        real_method = self.tested_class.post

        self.assertEqual(expected_method, real_method)

    def test_When_GetMethod_Should_ErrorWithStatus405(self):
        response = self.logged_client.get(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethod_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethod_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethod_Should_ErrorWithStatus405(self):
        response = self.logged_client.delete(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethod_Should_ReturnCommentAndStatus201(self):
        data = {
            'body': 'q' * 50,
            'commented_id': 'Q291cnNlVHlwZTox',
            'rating': 5,
        }
        response = self.logged_client.post(self.url, data=data)
        serializer = self.serializer_class(Comment.objects.last())

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = serializer.data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
