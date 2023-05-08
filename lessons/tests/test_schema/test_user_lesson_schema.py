from datetime import timedelta

from django.utils import timezone
from graphene import Context, DateTime, Int, Schema
from graphene.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.UserLesson import UserLesson
from ...schema.UserLessonType import UserLessonQuery, UserLessonType


class UserLessonTypeTestCase(JSONWebTokenTestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserLessonType

        first_user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': first_user,
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

        parent_lesson = Lesson.objects.create(**{
            'id': 1,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME,
        })

        first_lesson = Lesson.objects.create(**{
            'id': 2,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY,
        })

        second_lesson = Lesson.objects.create(**{
            'id': 3,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY,
        })

        UserLesson.objects.create(**{
            'id': 1,
            'lesson': parent_lesson,
            'user': first_user,
            'completed_at': timezone.now() - timedelta(days=1),
        })

        UserLesson.objects.create(**{
            'id': 2,
            'lesson': first_lesson,
            'user': first_user,
            'completed_at': timezone.now() - timedelta(days=1),
        })

        UserLesson.objects.create(**{
            'id': 3,
            'lesson': second_lesson,
            'user': first_user,
            'completed_at': timezone.now() - timedelta(days=7),
        })

        context = Context()
        context.user = first_user
        cls.context = context

    def setUp(self):
        schema = Schema(query=UserLessonQuery)
        self.gql_client = Client(schema=schema)

    def test_Should_IncludeDefiniteFieldsFromModel(self):
        expected_fields = [
            'completed_at', 'count_lesson',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'completed_at': DateTime,
            'count_lesson': Int,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_When_SendQueryWithNotAuthenticate_Should_ErrorHasNotPermission(
            self):
        response = self.client.execute(
            """
            query {
                myLessonHistory {
                    completedAt
                    countLesson
                }
            }
            """
        )

        expected_data = {
            'data': {
                'myLessonHistory': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': ['myLessonHistory', ],
                },
            ],
        }
        real_data = response.formatted

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithNotValidLessonID_Should_ErrorNotValidLessonID(
            self):
        response = self.gql_client.execute(
            """
            query {
                myLessonHistory {
                    completedAt
                    countLesson
                }
            }
            """,
            context=self.context,
        )

        history_lesson = [
            {
                'completedAt': str(
                    (timezone.now() - timedelta(days=6 - i)).date()
                ),
                'countLesson': 0,
            } for i in range(7)
        ]
        history_lesson[-2]['countLesson'] = 1

        expected_data = {
            'data': {
                'myLessonHistory': history_lesson,
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
