from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from ...models.Comment import Comment
from ...serializers.CommentEventSerializer import CommentEventSerializer
from ...views.CommentEventView import CommentEventView


class CommentEventViewTest(APITestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CommentEventView
        cls.serializer_class = CommentEventSerializer

        user = User.objects.create_user(email='test@email.com',
                                        password='password')

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

    def test_Should_SerializerClassIsCommentEventSerializer(self):
        expected_super_classes = 'CommentEventSerializer'
        real_super_classes = self.tested_class.serializer_class.__name__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_When_GetMethod_Should_ErrorWithStatus405(self):
        url = reverse('comments-event')
        response = self.logged_client.get(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethod_Should_ErrorWithStatus405(self):
        url = reverse('comments-event')
        response = self.logged_client.put(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethod_Should_ErrorWithStatus405(self):
        url = reverse('comments-event')
        response = self.logged_client.patch(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethod_Should_ErrorWithStatus405(self):
        url = reverse('comments-event')
        response = self.logged_client.delete(url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethod_Should_ReturnCommentAndStatus201(self):
        data = {
            'body': 'q' * 50,
            'commented_id': 'OjE=',
        }

        url = reverse('comments-event')
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
