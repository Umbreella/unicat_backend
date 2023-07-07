from django.db import connections
from django.test import TestCase
from django.utils import timezone
from django.utils.connection import ConnectionProxy

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.LearningFormat import LearningFormat
from ...tasks.UpdateCourseCountListenersTask import \
    update_course_count_listeners_task


class UpdateCourseCountListenersTaskTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_task = update_course_count_listeners_task

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
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        with ConnectionProxy(connections, 'master').cursor() as c:
            c.execute("""
                INSERT INTO courses_usercourse(
                    course_id,
                    user_id,
                    count_independents_completed,
                    count_lectures_completed,
                    last_view,
                    created_at
                )
                VALUES (1, 1, 0, 0, '%s', '%s');
            """ % (
                timezone.now(),
                timezone.now(),
            ))

    def test_When_TaskIsCalled_Should_CountListenersInCourse(self):
        task = self.tested_task.apply_async(kwargs={
            'course_id': self.course.id,
        })
        self.course.refresh_from_db()

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_count_listeners = 1
        real_count_listeners = self.course.count_listeners

        expected_result = 'Course count_listeners is updated.'
        real_result = str(task.result)

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_count_listeners, real_count_listeners)
        self.assertEqual(expected_result, real_result)
