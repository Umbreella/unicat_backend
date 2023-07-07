from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from courses.models.UserCourse import UserCourse
from users.models import User
from users.models.Teacher import Teacher

from ...tasks.UpdateUserCourseLastViewTask import \
    update_user_course_last_view_task


class UpdateUserCourseLastViewTaskTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_task = update_user_course_last_view_task

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
            'id': 1,
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

        cls.user_course = UserCourse.objects.create(**{
            'user': user,
            'course': course,
            'last_view': timezone.now() - timedelta(days=2),
        })

        cls.date_format = '%H-%M %d-%m-%Y'

    def test_When_LessonIdIsNotFound_Should_StatusIsSUCCESS(self):
        task = self.tested_task.apply_async(kwargs={
            'user_course_id': 1,
        })
        self.user_course.refresh_from_db()

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_last_view = timezone.now().strftime(self.date_format)
        real_last_view = self.user_course.last_view.strftime(self.date_format)

        expected_result = 'UserCourse last_view is updated.'
        real_result = str(task.result)

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_last_view, real_last_view)
        self.assertEqual(expected_result, real_result)
