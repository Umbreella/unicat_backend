from django.test import TestCase
from rest_framework.permissions import BasePermission

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from courses.models.UserCourse import UserCourse
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...permissions.HasLessonPermission import HasLessonPermission


class HasLessonPermissionTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = HasLessonPermission

        user = User.objects.create_superuser(**{
            'email': 'test@email.com',
            'password': 'password',
        })

        teacher = Teacher.objects.create(**{
            'user': user,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        first_course = Course.objects.create(**{
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

        second_course = Course.objects.create(**{
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

        Lesson.objects.create(**{
            'id': 1,
            'course': first_course,
            'title': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME.value,
            'description': 'q' * 50,
        })

        Lesson.objects.create(**{
            'id': 2,
            'course': second_course,
            'title': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME.value,
            'description': 'q' * 50,
        })

        UserCourse.objects.create(**{
            'user': user,
            'course': first_course,
        })

        cls.request = type('request', (object,), {'user': user, })

        cls.view = type('view', (object,), {
            'kwargs': {
                'lesson_id': 'TGVzc29uVHlwZTox',
            },
        })

    def test_Should_InheritBasePermission(self):
        expected_super_classes = (
            BasePermission,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_When_LessonIdNotValid_Should_AccessDenied(self):
        view = self.view
        view.kwargs.update({
            'lesson_id': 'q' * 50,
        })

        expected_permission = False
        real_permission = self.tested_class().has_permission(**{
            'request': self.request,
            'view': view,
        })

        self.assertEqual(expected_permission, real_permission)

    def test_When_LessonIdNotFound_Should_AccessDenied(self):
        view = self.view
        view.kwargs.update({
            'lesson_id': 'TGVzc29uVHlwZToz',
        })

        expected_permission = False
        real_permission = self.tested_class().has_permission(**{
            'request': self.request,
            'view': view,
        })

        self.assertEqual(expected_permission, real_permission)

    def test_When_LessonIdHasNotAccess_Should_AccessDenied(self):
        view = self.view
        view.kwargs.update({
            'lesson_id': 'TGVzc29uVHlwZToy',
        })

        expected_permission = False
        real_permission = self.tested_class().has_permission(**{
            'request': self.request,
            'view': view,
        })

        self.assertEqual(expected_permission, real_permission)

    def test_When_LessonIdHasAccess_Should_AccessAllowed(self):
        view = self.view

        expected_permission = True
        real_permission = self.tested_class().has_permission(**{
            'request': self.request,
            'view': view,
        })

        expected_view_kwargs = {
            'lesson_id': 1,
        }
        real_view_kwargs = view.kwargs

        self.assertEqual(expected_permission, real_permission)
        self.assertEqual(expected_view_kwargs, real_view_kwargs)
