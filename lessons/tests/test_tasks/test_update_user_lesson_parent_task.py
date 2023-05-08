from datetime import timedelta

from django.db import connections
from django.test import TestCase
from django.utils import timezone
from django.utils.connection import ConnectionProxy

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.UserLesson import UserLesson
from ...tasks.UpdateUserLessonParentTask import update_user_lesson_parent_task


class UpdateUserLessonParentTaskTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_task = update_user_lesson_parent_task

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
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        parent_lesson = Lesson.objects.create(**{
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
            'lesson_type': LessonTypeChoices.TEST.value,
            'count_questions': 50,
            'parent': parent_lesson,
        })

        Lesson.objects.create(**{
            'id': 3,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST.value,
            'count_questions': 50,
        })

        cls.user_lesson = UserLesson.objects.create(**{
            'lesson': parent_lesson,
            'user': user,
            'completed_at': None,
        })

        with ConnectionProxy(connections, 'master').cursor() as c:
            c.execute("""
            INSERT INTO lessons_userlesson(
                completed_at, lesson_id, user_id
            )
            VALUES ('%s', 2, 1);
            """ % (
                (timezone.now() - timedelta(days=1)).date(),
            ))

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

        expected_result = 'Nothing can be done with this "lesson_id".'
        real_result = str(task.result)

        expected_completed_at = None
        real_completed_at = self.user_lesson.completed_at

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_result, real_result)
        self.assertEqual(expected_completed_at, real_completed_at)

    def test_When_ParentIsNone_Should_DontUpdateParent(self):
        task = self.tested_task.apply_async(kwargs={
            'lesson_id': 3,
            'user_id': 1,
        })

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_result = 'Nothing can be done with this "lesson_id".'
        real_result = str(task.result)

        expected_completed_at = None
        real_completed_at = self.user_lesson.completed_at

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_result, real_result)
        self.assertEqual(expected_completed_at, real_completed_at)

    def test_When_UserIsNotFound_Should_StatusIsFAILURE(self):
        task = self.tested_task.apply_async(kwargs={
            'lesson_id': 2,
            'user_id': 2,
        })
        self.user_lesson.refresh_from_db()

        expected_state = 'FAILURE'
        real_state = task.state

        expected_result = str({
            'user': [
                'user instance with id 2 does not exist.',
            ],
        })
        real_result = str(task.result)

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_result, real_result)

    def test_When_LessonIsValid_Should_UpdateUserLessonParent(self):
        task = self.tested_task.apply_async(kwargs={
            'lesson_id': 2,
            'user_id': 1,
        })
        self.user_lesson.refresh_from_db()

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_result = 'Parent Lesson is updated.'
        real_result = str(task.result)

        expected_completed_at = None
        real_completed_at = self.user_lesson.completed_at

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_result, real_result)
        self.assertNotEqual(expected_completed_at, real_completed_at)

    def test_When_LessonIsValid_Should_CreateUserLessonParent(self):
        self.user_lesson.delete()
        task = self.tested_task.apply_async(kwargs={
            'lesson_id': 2,
            'user_id': 1,
        })
        user_lesson = UserLesson.objects.get(**{
            'lesson_id': 1,
        })

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_result = 'Parent Lesson is updated.'
        real_result = str(task.result)

        expected_completed_at = None
        real_completed_at = user_lesson.completed_at

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_result, real_result)
        self.assertNotEqual(expected_completed_at, real_completed_at)

    def test_When_NotAllLessonViewed_Should_DontUpdateParent(self):
        Lesson.objects.filter(id=3).update(parent_id=1)

        task = self.tested_task.apply_async(kwargs={
            'lesson_id': 2,
            'user_id': 1,
        })
        self.user_lesson.refresh_from_db()

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_result = 'Parent Lesson is not updated.'
        real_result = str(task.result)

        expected_completed_at = None
        real_completed_at = self.user_lesson.completed_at

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_result, real_result)
        self.assertEqual(expected_completed_at, real_completed_at)

    def test_When_NotAllLessonIsComplete_Should_DontUpdateParent(self):
        Lesson.objects.filter(id=3).update(parent_id=1)
        UserLesson.objects.create(**{
            'lesson_id': 3,
            'user_id': 1,
            'completed_at': None,
        })

        task = self.tested_task.apply_async(kwargs={
            'lesson_id': 2,
            'user_id': 1,
        })
        self.user_lesson.refresh_from_db()

        expected_state = 'SUCCESS'
        real_state = task.state

        expected_result = 'Parent Lesson is not updated.'
        real_result = str(task.result)

        expected_completed_at = None
        real_completed_at = self.user_lesson.completed_at

        self.assertEqual(expected_state, real_state)
        self.assertEqual(expected_result, real_result)
        self.assertEqual(expected_completed_at, real_completed_at)
