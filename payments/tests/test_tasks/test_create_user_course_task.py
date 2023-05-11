from django.test import TestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from courses.models.UserCourse import UserCourse
from users.models import User
from users.models.Teacher import Teacher

from ...tasks.CreateUserCourseTask import create_user_course_task


class UpdateCountLessonTaskTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_task = create_user_course_task

        user = User.objects.create_user(**{
            'id': 1,
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
            'id': 1,
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

    def test_When_DataIsValid_Should_StatusIsSUCCESS(self):
        task = self.tested_task.apply_async(kwargs={
            'course_id': 1,
            'user_id': 1,
        })

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_result = {
            'id': 1,
            'course_id': 1,
            'user_id': 1,
        }
        real_result = UserCourse.objects.values(
            'id', 'course_id', 'user_id',
        ).last()

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_result, real_result)
