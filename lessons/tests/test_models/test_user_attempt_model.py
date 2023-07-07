from datetime import timedelta

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models import (BigAutoField, DateTimeField, ForeignKey,
                              ManyToOneRel, PositiveSmallIntegerField)
from django.test import TestCase
from django.utils import timezone

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.UserAttempt import UserAttempt
from ...models.UserLesson import UserLesson


class UserAttemptTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserAttempt

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
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        cls.lesson_without_time_limit = Lesson.objects.create(**{
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST,
            'count_questions': 10,
        })

        lesson_with_time_limit = Lesson.objects.create(**{
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST,
            'time_limit': timedelta(minutes=10),
            'count_questions': 10,
        })

        cls.user_lesson_without_time_limit = UserLesson.objects.create(**{
            'lesson': cls.lesson_without_time_limit,
            'user': user,
        })

        user_lesson_with_time_limit = UserLesson.objects.create(**{
            'lesson': lesson_with_time_limit,
            'user': user,
        })

        cls.data_without_time_limit = {
            'user_lesson': cls.user_lesson_without_time_limit,
        }

        cls.data_with_time_limit = {
            'user_lesson': user_lesson_with_time_limit,
        }

        cls.date_format = '%H:%M %d-%m-%Y'
        cls.cache_key = 'VXNlckF0dGVtcHRUeXBlOjE=_answered_questions'

    @classmethod
    def setUp(cls):
        cache.clear()

    @classmethod
    def tearDown(cls):
        cache.clear()

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'user_answers', 'id', 'user_lesson', 'time_start', 'time_end',
            'count_true_answer',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'user_answers': ManyToOneRel,
            'id': BigAutoField,
            'user_lesson': ForeignKey,
            'time_start': DateTimeField,
            'time_end': DateTimeField,
            'count_true_answer': PositiveSmallIntegerField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'count_true_answer': 'The number of correct answers.',
            'id': '',
            'time_end': 'Attempt completion time.',
            'time_start': 'Attempt start time.',
            'user_answers': '',
            'user_lesson': 'The user lesson to which the attempt is attached.',
        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreateUserAttemptWithOutData_Should_ErrorBlankFields(self):
        user_attempt = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            user_attempt.save()

        expected_raise = {
            'user_lesson': [
                'This field cannot be null.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_CreateUserAttemptWithOutTimeLimit_Should_TimeEndIsNone(self):
        data = self.data_without_time_limit

        user_attempt = self.tested_class(**data)
        user_attempt.save()

        expected_time_start = timezone.now().strftime(self.date_format)
        real_time_start = user_attempt.time_start.strftime(self.date_format)

        expected_time_end = None
        real_time_end = user_attempt.time_end

        self.assertEqual(expected_time_start, real_time_start)
        self.assertEqual(expected_time_end, real_time_end)

    def test_When_CreateUserAttemptWithTimeLimit_Should_TimeEndAsSumTime(self):
        data = self.data_with_time_limit

        user_attempt = self.tested_class(**data)
        user_attempt.save()

        time_end = timezone.now() + timedelta(minutes=10)

        expected_time_end = time_end.strftime(self.date_format)
        real_time_end = user_attempt.time_end.strftime(self.date_format)

        self.assertEqual(expected_time_end, real_time_end)

    def test_When_NotAllQuestionsInCache_Should_DontUpdateTimeEnd(self):
        data = self.data_with_time_limit

        user_attempt = self.tested_class(**data)
        user_attempt.save()

        expected_time_end = user_attempt.time_end.strftime(self.date_format)

        cache.set(self.cache_key, [1] * 7)
        user_attempt.save()

        real_time_end = user_attempt.time_end.strftime(self.date_format)

        self.assertEqual(expected_time_end, real_time_end)

    def test_When_AllQuestionsInCache_Should_UpdateTimeEnd(self):
        data = self.data_with_time_limit

        user_attempt = self.tested_class(**data)
        user_attempt.save()

        cache.set(self.cache_key, [1] * 10)
        user_attempt.save()

        expected_time_end = timezone.now().strftime(self.date_format)
        real_time_end = user_attempt.time_end.strftime(self.date_format)

        self.assertEqual(expected_time_end, real_time_end)

    def test_When_UpdateUserAttempt_Should_DontUpdateTimeEnd(self):
        data = self.data_with_time_limit

        user_attempt = self.tested_class(**data)
        user_attempt.save()

        expected_time_end = user_attempt.time_end.strftime(self.date_format)

        user_attempt.count_true_answer = 1
        user_attempt.save()

        real_time_end = user_attempt.time_end.strftime(self.date_format)

        self.assertEqual(expected_time_end, real_time_end)

    def test_When_SaveUserAttemptForCompletedLesson_Should_DontUpdateCompleted(
            self):
        user_lesson = self.user_lesson_without_time_limit
        user_lesson.completed_at = timezone.now()
        user_lesson.save()

        data = self.data_without_time_limit

        user_attempt = self.tested_class(**data)
        user_attempt.save()

        expected_completed_at = timezone.now().date().strftime(
            self.date_format)
        real_completed_at = user_lesson.completed_at.strftime(self.date_format)

        self.assertEqual(expected_completed_at, real_completed_at)

    def test_When_LessonIsCompletedAndAttemptIsSuccess_Should_DontUpdateLesson(
            self):
        time_now = timezone.now()

        self.user_lesson_without_time_limit.completed_at = time_now
        self.user_lesson_without_time_limit.save()

        data = self.data_without_time_limit

        user_attempt = self.tested_class(**data)
        user_attempt.save()

        user_attempt.count_true_answer = 10
        user_attempt.save()

        user_lesson = user_attempt.user_lesson
        user_lesson.refresh_from_db()

        expected_completed_at = time_now.date().strftime(self.date_format)
        real_completed_at = user_lesson.completed_at.strftime(self.date_format)

        self.assertEqual(expected_completed_at, real_completed_at)

    def test_When_CountTrueAnswersGreater60Percent_Should_UpdateUserLesson(
            self):
        data = self.data_without_time_limit

        user_attempt = self.tested_class(**data)
        user_attempt.save()

        user_attempt.count_true_answer = 6
        user_attempt.save()

        user_lesson = user_attempt.user_lesson
        user_lesson.refresh_from_db()

        expected_completed_at = timezone.now().date().strftime(
            self.date_format
        )
        real_completed_at = user_lesson.completed_at.strftime(self.date_format)

        self.assertEqual(expected_completed_at, real_completed_at)

    def test_When_CountTrueAnswersLess60Percent_Should_DontUpdateUserLesson(
            self):
        data = self.data_without_time_limit
        data.update({
            'count_true_answer': 5,
        })

        user_attempt = self.tested_class(**data)
        user_attempt.save()

        user_lesson = user_attempt.user_lesson
        user_lesson.refresh_from_db()

        expected_completed_at = None
        real_completed_at = user_lesson.completed_at

        self.assertEqual(expected_completed_at, real_completed_at)
