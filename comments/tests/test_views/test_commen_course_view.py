from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Comment import Comment
from ...serializers.CommentCourseSerializer import CommentCourseSerializer
from ...views.CommentCourseView import CommentCourseView


class CommentCourseViewTest(APITestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CommentCourseView
        cls.serializer_class = CommentCourseSerializer

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
            'description': 'q' * 50,
        })

        client = cls.client_class()
        client.force_authenticate(user=user)

        cls.logged_client = client

    def test_Should_SuperClassIsCommentView(self):
        super_classes = self.tested_class.__bases__

        expected_super_classes = [
            'CommentView',
        ]
        real_super_classes = [_super.__name__ for _super in super_classes]

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_SerializerClassIsCommentCourseSerializer(self):
        expected_super_classes = 'CommentCourseSerializer'
        real_super_classes = self.tested_class.serializer_class.__name__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_When_GetMethod_Should_ErrorWithStatus405(self):
        url = reverse('comments-course')
        response = self.logged_client.get(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethod_Should_ErrorWithStatus405(self):
        url = reverse('comments-course')
        response = self.logged_client.put(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethod_Should_ErrorWithStatus405(self):
        url = reverse('comments-course')
        response = self.logged_client.patch(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethod_Should_ErrorWithStatus405(self):
        url = reverse('comments-course')
        response = self.logged_client.delete(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethod_Should_ReturnCommentAndStatus201(self):
        data = {
            'body': 'q' * 50,
            'commented_id': 'OjE=',
            'rating': 5,
        }

        url = reverse('comments-course')
        response = self.logged_client.post(url, data=data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        created_comment = Comment.objects.last()
        serializer = self.serializer_class(data=data,
                                           instance=created_comment)
        serializer.is_valid()

        expected_data = serializer.data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
