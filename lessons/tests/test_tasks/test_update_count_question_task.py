from django.db import connections
from django.test import TestCase
from django.utils.connection import ConnectionProxy

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...tasks.UpdateCountQuestionTask import update_count_question_task


class UpdateCountQuestionTaskTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_task = update_count_question_task

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

        cls.lesson = Lesson.objects.create(**{
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST.value,
            'count_questions': 50,
        })

        with ConnectionProxy(connections, 'master').cursor() as c:
            c.execute("""
            INSERT INTO lessons_question(
                body,
                question_type,
                lesson_id
            )
            VALUES ('q', 1, 1);
            """)

    def test_When_LessonIdIsValid_Should_UpdateCountQuestion(self):
        task = self.tested_task.apply_async(kwargs={
            'lesson_id': 1,
        })

        self.lesson.refresh_from_db()

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_count_questions = 1
        real_count_questions = self.lesson.count_questions

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_count_questions, real_count_questions)
