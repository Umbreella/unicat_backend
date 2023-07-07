from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from events.models.New import New
from users.models import User

from ...models.Comment import Comment
from ...serializers.CreateCommentNewsSerializer import \
    CreateCommentNewsSerializer
from ...views.CreateCommentNewsView import CreateCommentNewsView
from ...views.CreateCommentView import CreateCommentView


class CreateCommentNewsViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CreateCommentNewsView
        cls.serializer_class = CreateCommentNewsSerializer
        cls.url = reverse('create_comment_news')

        user = User.objects.create_user(email='test@email.com',
                                        password='password')

        New.objects.create(**{
            'preview': 'temporary_img',
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'author': user,
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

    def test_Should_SerializerClassIsCommentNewsSerializer(self):
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

    def test_When_PostMethod_Should_ReturnCommentWithStatus201(self):
        data = {
            'body': 'q' * 50,
            'commented_id': 'TmV3VHlwZTox',
        }
        response = self.logged_client.post(self.url, data=data)
        serializer = self.serializer_class(Comment.objects.last())

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = serializer.data
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
