from django.db import connections
from django.test import TestCase
from django.utils.connection import ConnectionProxy

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.LearningFormat import LearningFormat
from ...tasks.UpdateTeacherInfoTask import update_teacher_info_task


class UpdateTeacherTaskTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_task = update_teacher_info_task

        user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        cls.teacher = Teacher.objects.create(**{
            'user': user,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        Course.objects.create(**{
            'id': 1,
            'teacher': cls.teacher,
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
                UPDATE courses_course
                SET avg_rating = 4.5
                WHERE id = 1;
            """)
            c.execute("""
                UPDATE courses_coursestat
                SET count_comments = 10
                WHERE id = 1;
            """)

    def test_When_TaskIsCalled_Should_UpdateRatingAndCountReviews(self):
        task = self.tested_task.apply_async(kwargs={
            'teacher_id': self.teacher.id,
        })
        self.teacher.refresh_from_db()

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_rating = 4.5
        real_rating = self.teacher.avg_rating

        expected_count_reviews = 10
        real_count_reviews = self.teacher.count_reviews

        expected_result = 'Teacher info is updated.'
        real_result = str(task.result)

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_rating, real_rating)
        self.assertEqual(expected_count_reviews, real_count_reviews)
        self.assertEqual(expected_result, real_result)
