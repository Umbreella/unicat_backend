import json
from datetime import timedelta

from django.utils import timezone
from graphene import Boolean, Float, NonNull, String, relay
from graphene_django.utils import GraphQLTestCase
from rest_framework_simplejwt.tokens import RefreshToken

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from courses.models.UserCourse import UserCourse
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonBody import LessonBody
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.UserLesson import UserLesson
from ...schema.LessonType import LessonType


class LessonTypeTestCase(GraphQLTestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LessonType
        cls.model = Lesson

        cls.user_access = User.objects.create_superuser(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        cls.user_not_access = User.objects.create_superuser(**{
            'email': 'w' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': cls.user_access,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        course_with_access = Course.objects.create(**{
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

        course_with_out_access = Course.objects.create(**{
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

        lesson_with_body_complete = Lesson.objects.create(**{
            'id': 1,
            'course': course_with_access,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME,
        })

        Lesson.objects.create(**{
            'id': 2,
            'course': course_with_access,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME,
        })

        Lesson.objects.create(**{
            'id': 3,
            'course': course_with_out_access,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME,
        })

        UserLesson.objects.create(**{
            'user': cls.user_access,
            'lesson': lesson_with_body_complete,
            'completed_at': timezone.now(),
        })

        cls.lesson_body = LessonBody.objects.create(**{
            'lesson': lesson_with_body_complete,
            'body': 'q' * 50,
        })

        cls.user_course = UserCourse.objects.create(**{
            'user': cls.user_access,
            'course': course_with_access,
            'last_view': timezone.now() - timedelta(days=2),
        })

        cls.date_format = '%H-%M %d-%m-%Y'

    def test_Should_IncludeDefiniteDjangoModel(self):
        expected_model = self.model
        real_model = self.tested_class._meta.model

        self.assertEqual(expected_model, real_model)

    def test_Should_IncludeDefiniteInterfaces(self):
        expected_interfaces = [
            relay.Node,
        ]
        real_interfaces = list(self.tested_class._meta.interfaces)

        self.assertEqual(expected_interfaces, real_interfaces)

    def test_Should_IncludeDefiniteFieldsFromModel(self):
        expected_fields = [
            'id', 'serial_number', 'title', 'description', 'lesson_type',
            'time_limit', 'count_questions', 'is_completed', 'body',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'body': String,
            'lesson_type': String,
            'serial_number': String,
            'is_completed': Boolean,
            'time_limit': Float,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(field).__class__ == NonNull for field in [
                'id', 'title', 'description', 'count_questions',
            ]
        ])

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)

    def test_When_SendQueryWithOutAuthenticate_Should_ErrorHasNotPermission(
            self):
        response = self.query(
            """
            query {
                lesson (id: "TGVzc29uVHlwZToz") {
                    id
                }
            }
            """,
        )

        expected_response = {
            'data': {
                'lesson': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': ['lesson', ],
                },
            ],
        }
        real_response = json.loads(response.content)

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithOutAccess_Should_ErrorNotHaveAccess(self):
        refresh_token = RefreshToken.for_user(self.user_not_access)
        response = self.query(
            """
            query {
                lesson (id: "TGVzc29uVHlwZToz") {
                    id
                    body
                }
            }
            """,
            headers={
                'HTTP_AUTHORIZATION': f'Bearer {refresh_token.access_token}',
            },
        )

        expected_response = {
            'data': {
                'lesson': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'You do not have access to this lesson.',
                    'path': ['lesson', ],
                },
            ],
        }
        real_response = json.loads(response.content)

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithAccess_Should_ReturnLessonAndLessonBody(self):
        access_token = RefreshToken.for_user(self.user_access).access_token
        response = self.query(
            """
            query {
                lesson (id: "TGVzc29uVHlwZTox") {
                    id
                    body
                    lessonType
                    isCompleted
                    serialNumber
                }
            }
            """,
            headers={
                'HTTP_AUTHORIZATION': f'Bearer {access_token}',
            },
        )
        self.user_course.refresh_from_db()

        expected_response = {
            'data': {
                'lesson': {
                    'id': 'TGVzc29uVHlwZTox',
                    'body': self.lesson_body.body,
                    'lessonType': 'Тема',
                    'isCompleted': True,
                    'serialNumber': '1.',
                },
            },
        }
        real_response = json.loads(response.content)

        expected_last_view = timezone.now().strftime(self.date_format)
        real_last_view = self.user_course.last_view.strftime(self.date_format)

        self.assertEqual(expected_response, real_response)
        self.assertEqual(expected_last_view, real_last_view)

    def test_When_SendQueryLessonWithOutLessonBody_Should_ReturnLessonAndNull(
            self):
        access_token = RefreshToken.for_user(self.user_access).access_token
        response = self.query(
            """
            query {
                lesson (id: "TGVzc29uVHlwZToy") {
                    id
                    body
                    isCompleted
                }
            }
            """,
            headers={
                'HTTP_AUTHORIZATION': f'Bearer {access_token}',
            },
        )

        expected_response = {
            'data': {
                'lesson': {
                    'id': 'TGVzc29uVHlwZToy',
                    'body': None,
                    'isCompleted': False,
                },
            },
        }
        real_response = json.loads(response.content)

        self.assertEqual(expected_response, real_response)
