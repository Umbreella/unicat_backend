from django.db import connections
from django.test import TestCase
from django.utils import timezone
from django.utils.connection import ConnectionProxy

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from courses.models.UserCourse import UserCourse
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...tasks.UpdateUserCourseCountTask import update_user_course_count_task


class UpdateUserLessonParentTaskTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_task = update_user_course_count_task

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
            'count_lectures': 1,
            'count_independents': 1,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        Lesson.objects.create(**{
            'id': 1,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME.value,
            'count_questions': 50,
        })

        Lesson.objects.create(**{
            'id': 2,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY.value,
            'count_questions': 50,
        })

        Lesson.objects.create(**{
            'id': 3,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST.value,
            'count_questions': 50,
        })

        cls.user_course = UserCourse.objects.create(**{
            'course': course,
            'user': user,
        })

        with ConnectionProxy(connections, 'master').cursor() as c:
            c.execute("""
            INSERT INTO lessons_userlesson(
                completed_at, lesson_id, user_id
            )
            VALUES ('%s', 1, 1);
            """ % (
                timezone.now().date()
            ))
            c.execute("""
            INSERT INTO lessons_userlesson(
                completed_at, lesson_id, user_id
            )
            VALUES ('%s', 2, 1);
            """ % (
                timezone.now().date()
            ))
            c.execute("""
            INSERT INTO lessons_userlesson(
                completed_at, lesson_id, user_id
            )
            VALUES ('%s', 3, 1);
            """ % (
                timezone.now().date()
            ))
        cls.format = '%H-%M %d-%m-%Y'

    def test_When_LessonIdIsNotFound_Should_StatusIsFAILURE(self):
        task = self.tested_task.apply_async(kwargs={
            'lesson_id': 4,
            'user_id': 1,
        })

        expected_state = 'FAILURE'
        real_state = task.state

        expected_result = 'Lesson matching query does not exist.'
        real_result = str(task.result)

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_result, real_result)

    def test_When_LessonTypeIsTheme_Should_DontUpdateParent(self):
        task = self.tested_task.apply_async(kwargs={
            'lesson_id': 1,
            'user_id': 1,
        })

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_result = 'User Course is not updated.'
        real_result = str(task.result)

        expected_is_completed = None
        real_is_completed = self.user_course.completed_at

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_result, real_result)
        self.assertEqual(expected_is_completed, real_is_completed)

    def test_When_CompleteOnlyTheory_Should_UpdateButDontCompleteUserCourse(
            self):
        task = self.tested_task.apply_async(kwargs={
            'lesson_id': 2,
            'user_id': 1,
        })
        self.user_course.refresh_from_db()

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_count_lectures = 1
        real_count_lectures = self.user_course.count_lectures_completed

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_count_lectures, real_count_lectures)

    def test_When_CompleteOnlyTest_Should_UpdateButDontCompleteUserCourse(
            self):
        task = self.tested_task.apply_async(kwargs={
            'lesson_id': 3,
            'user_id': 1,
        })
        self.user_course.refresh_from_db()

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_count_independents = 1
        real_count_independents = self.user_course.count_independents_completed

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_count_independents, real_count_independents)
