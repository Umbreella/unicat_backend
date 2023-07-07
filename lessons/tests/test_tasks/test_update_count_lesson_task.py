from django.db import connections
from django.test import TestCase
from django.utils.connection import ConnectionProxy

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...tasks.UpdateCountLessonTask import update_count_lesson_task


class UpdateCountLessonTaskTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_task = update_count_lesson_task

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
            INSERT INTO lessons_lesson(
                serial_number,
                title,
                description,
                lesson_type,
                count_questions,
                course_id
            )
            VALUES (1, 'q', 'q', 2, 0, 1);
            """)
            c.execute("""
            INSERT INTO lessons_lesson(
                serial_number,
                title,
                description,
                lesson_type,
                count_questions,
                course_id
            )
            VALUES (1, 'q', 'q', 3, 0, 1);
            """)

    def test_When_LessonTypeIsNotValid_Should_StatusIsFAILURE(self):
        task = self.tested_task.apply_async(kwargs={
            'course_id': 1,
            'lesson_type': 4,
        })

        expected_state = 'FAILURE'
        real_state = task.state

        expected_result = '"lesson_type" is not valid.'
        real_result = str(task.result)

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_result, real_result)

    def test_When_LessonTypeIsTheme_Should_DontUpdateData(self):
        task = self.tested_task.apply_async(kwargs={
            'course_id': 1,
            'lesson_type': 1,
        })

        self.course.refresh_from_db()

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_result = 'Count lesson is not updated.'
        real_result = str(task.result)

        expected_count_lectures = 50
        real_count_lectures = self.course.count_lectures

        expected_count_independents = 50
        real_count_independents = self.course.count_independents

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_result, real_result)
        self.assertEqual(expected_count_lectures, real_count_lectures)
        self.assertEqual(expected_count_independents, real_count_independents)

    def test_When_LessonTypeIsTheory_Should_UpdateCountLectures(self):
        task = self.tested_task.apply_async(kwargs={
            'course_id': 1,
            'lesson_type': 2,
        })

        self.course.refresh_from_db()

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_count_lectures = 1
        real_count_lectures = self.course.count_lectures

        expected_count_independents = 50
        real_count_independents = self.course.count_independents

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_count_lectures, real_count_lectures)
        self.assertEqual(expected_count_independents, real_count_independents)

    def test_When_LessonTypeIsTest_Should_UpdateCountIndependents(self):
        task = self.tested_task.apply_async(kwargs={
            'course_id': 1,
            'lesson_type': 3,
        })

        self.course.refresh_from_db()

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_count_lectures = 50
        real_count_lectures = self.course.count_lectures

        expected_count_independents = 1
        real_count_independents = self.course.count_independents

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_count_lectures, real_count_lectures)
        self.assertEqual(expected_count_independents, real_count_independents)
