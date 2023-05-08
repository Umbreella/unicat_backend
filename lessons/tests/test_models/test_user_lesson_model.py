from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from courses.models.UserCourse import UserCourse
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.UserLesson import UserLesson


class UserLessonTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserLesson

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

        cls.user_course = UserCourse.objects.create(**{
            'course': course,
            'user': user,
        })

        parent_lesson = Lesson.objects.create(**{
            'id': 1,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME,
        })

        lesson = Lesson.objects.create(**{
            'id': 2,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY,
            'parent': parent_lesson,
        })

        cls.data = {
            'lesson': lesson,
            'user': user,
        }

        cls.format = '%H-%M %d-%m-%Y'

    def test_When_CreateUserLessonWithOutData_Should_ErrorBlankFields(self):
        user_lesson = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            user_lesson.save()

        expected_raise = {
            'lesson': [
                'This field cannot be null.',
            ],
            'user': [
                'This field cannot be null.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_CreateUserLessonWithValidData_Should_SaveUserLesson(self):
        data = self.data

        user_lesson = self.tested_class(**data)
        user_lesson.save()

        expected_completed_at = None
        real_completed_at = user_lesson.completed_at

        self.assertEqual(expected_completed_at, real_completed_at)

    def test_When_CreateDuplicateUserLesson_Should_ErrorNotUniqueFields(self):
        data = self.data

        user_lesson = self.tested_class(**data)
        user_lesson.save()

        user_lesson_duplicate = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            user_lesson_duplicate.save()

        expected_raise = {
            '__all__': [
                'User lesson with this Lesson and User already exists.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataIsValid_Should_CreateUserLesson(self):
        data = self.data
        data.update({
            'completed_at': timezone.now(),
        })

        user_lesson = self.tested_class(**data)
        user_lesson.save()
        self.user_course.refresh_from_db()

        expected_count_user_lesson = 2
        real_count_user_lesson = len(UserLesson.objects.all())

        expected_completed_at = None
        real_completed_at = UserLesson.objects.get(**{
            'lesson_id': 1,
        }).completed_at

        expected_count_lectures = 1
        real_count_lectures = self.user_course.count_lectures_completed

        self.assertEqual(expected_count_user_lesson, real_count_user_lesson)
        self.assertNotEqual(expected_completed_at, real_completed_at)
        self.assertEqual(expected_count_lectures, real_count_lectures)
