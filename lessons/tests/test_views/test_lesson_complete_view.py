from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APITestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from courses.models.UserCourse import UserCourse
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...permissions.HasLessonPermission import HasLessonPermission
from ...serializers.LessonCompleteSerializer import LessonCompleteSerializer
from ...views.LessonCompleteView import LessonCompleteView


class LessonCompleteViewTestCase(APITestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LessonCompleteView
        cls.serializer = LessonCompleteSerializer
        cls.tested_url = reverse('lesson_complete',
                                 kwargs={'lesson_id': 'TGVzc29uVHlwZTox', })

        user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': user,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        course = Course.objects.create(**{
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

        Lesson.objects.create(**{
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY,
        })

        UserCourse.objects.create(**{
            'course': course,
            'user': user,
        })

        client = cls.client_class()
        client.force_authenticate(user=user)
        cls.logged_client = client

    def test_Should_PermissionClassesIsAuthenticated(self):
        expected_classes = (
            IsAuthenticated, HasLessonPermission,
        )
        real_classes = self.tested_class.permission_classes

        self.assertEqual(expected_classes, real_classes)

    def test_Should_SerializerClassIsLessonCompleteSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_When_GetMethod_Should_ErrorWithStatus405(self):
        response = self.logged_client.get(self.tested_url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethod_Should_ErrorWithStatus405(self):
        response = self.logged_client.put(self.tested_url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethod_Should_ErrorWithStatus405(self):
        response = self.logged_client.patch(self.tested_url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethod_Should_ErrorWithStatus405(self):
        response = self.logged_client.delete(self.tested_url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethod_Should_SaveLessonComplete(self):
        response = self.logged_client.post(self.tested_url, {})

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = {
            'data': 'Lesson is complete.',
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
