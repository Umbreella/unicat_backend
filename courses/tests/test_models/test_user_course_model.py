from django.core.exceptions import ValidationError
from django.db.models import (BigAutoField, DateTimeField, ForeignKey,
                              PositiveSmallIntegerField)
from django.test import TestCase
from django.utils import timezone

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.LearningFormat import LearningFormat
from ...models.UserCourse import UserCourse


class UserCourseTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserCourse

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

        cls.course = Course.objects.create(**{
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

        cls.data = {
            'course': cls.course,
            'user': user,
        }

        cls.date_format = '%H:%M %d/%m/%Y'

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'id', 'course', 'user', 'count_lectures_completed',
            'count_independents_completed', 'created_at', 'last_view',
            'completed_at',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'course': ForeignKey,
            'user': ForeignKey,
            'count_lectures_completed': PositiveSmallIntegerField,
            'count_independents_completed': PositiveSmallIntegerField,
            'created_at': DateTimeField,
            'last_view': DateTimeField,
            'completed_at': DateTimeField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'id': '',
            'user': 'The user who gained access.',
            'course': 'The course that has been accessed.',
            'count_independents_completed': (
                'The number of independent tasks performed by the user from '
                'the course, calculated automatically.'
            ),
            'count_lectures_completed': (
                'The number of lectures delivered by the user from the '
                'course, calculated automatically.'
            ),

            'completed_at': (
                'Have you completed enough lessons to consider the course '
                'completed at a minimum'
            ),
            'last_view': (
                'The date of the last viewing of the lesson from the course.'
            ),
            'created_at': 'Access creation time.',
        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreateUserCourseWithOutData_Should_ErrorBlankField(self):
        user_course = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            user_course.save()

        expected_raise = {
            'course': [
                'This field cannot be null.',
            ],
            'user': [
                'This field cannot be null.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_CreateUserCourseWithData_Should_CreateUserCourse(self):
        data = self.data
        timezone_now = timezone.now()

        user_course = self.tested_class(**data)
        user_course.save()
        self.course.refresh_from_db()

        user_course_dict = dict(user_course)
        created_at = user_course_dict.pop('created_at')
        last_view = user_course_dict.pop('last_view')

        expected_created_at = timezone_now.strftime(self.date_format)
        real_created_at = created_at.strftime(self.date_format)

        expected_last_view = timezone_now.strftime(self.date_format)
        real_last_view = last_view.strftime(self.date_format)

        expected_dict = {
            'id': 1,
            'course_id': 1,
            'user_id': 1,
            'count_lectures_completed': 0,
            'count_independents_completed': 0,
            'completed_at': None,
        }
        real_dict = user_course_dict

        expected_count_listeners = 1
        real_count_listeners = self.course.count_listeners

        self.assertEqual(expected_created_at, real_created_at)
        self.assertEqual(expected_last_view, real_last_view)
        self.assertEqual(expected_dict, real_dict)
        self.assertEqual(expected_count_listeners, real_count_listeners)

    def test_When_UserCompleteOnlyLectures_Should_DontSetCompleted(self):
        data = self.data
        data.update({
            'count_lectures_completed': 50,
        })

        user_course = self.tested_class(**data)
        user_course.save()

        expected_completed_at = None
        real_completed_at = user_course.completed_at

        self.assertEqual(expected_completed_at, real_completed_at)

    def test_When_UserCompleteOnlyIndependents_Should_DontSetCompleted(self):
        data = self.data
        data.update({
            'count_independents_completed': 50,
        })

        user_course = self.tested_class(**data)
        user_course.save()

        expected_completed_at = None
        real_completed_at = user_course.completed_at

        self.assertEqual(expected_completed_at, real_completed_at)

    def test_When_UserCompleteFullCourse_Should_SetCompletedOnNow(self):
        data = self.data
        data.update({
            'count_lectures_completed': 50,
            'count_independents_completed': 50,
        })
        timezone_now = timezone.now()

        user_course = self.tested_class(**data)
        user_course.save()

        expected_completed_at = timezone_now.strftime(self.date_format)
        real_completed_at = user_course.completed_at.strftime(self.date_format)

        self.assertEqual(expected_completed_at, real_completed_at)
