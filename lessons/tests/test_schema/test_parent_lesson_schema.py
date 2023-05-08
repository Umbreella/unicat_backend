from django.utils import timezone
from graphene import Boolean, Context, List, NonNull, Schema, String
from graphene.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from courses.models.UserCourse import UserCourse
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.UserLesson import UserLesson
from ...schema.ParentLessonType import ParentLessonQuery, ParentLessonType


class ParentLessonTypeTestCase(JSONWebTokenTestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = ParentLessonType
        cls.model = Lesson

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

        lesson_parent = Lesson.objects.create(**{
            'id': 1,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME,
        })

        Lesson.objects.create(**{
            'id': 2,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME,
        })

        Lesson.objects.create(**{
            'id': 3,
            'course': course,
            'parent': lesson_parent,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY,
        })

        UserCourse.objects.create(**{
            'course': course,
            'user': user,
        })

        UserLesson.objects.create(**{
            'lesson': lesson_parent,
            'user': user,
            'completed_at': timezone.now(),
        })

        #   'Q291cnNlVHlwZTox' - 'CourseType:1'
        cls.course_id = 'Q291cnNlVHlwZTox'

        context = Context()
        context.user = user
        cls.context = context

    def setUp(self):
        schema = Schema(query=ParentLessonQuery)
        self.gql_client = Client(schema=schema)

    def test_Should_IncludeDefiniteDjangoModel(self):
        expected_model = self.model
        real_model = self.tested_class._meta.model

        self.assertEqual(expected_model, real_model)

    def test_Should_IncludeDefiniteInterfaces(self):
        expected_interfaces = []
        real_interfaces = list(self.tested_class._meta.interfaces)

        self.assertEqual(expected_interfaces, real_interfaces)

    def test_Should_IncludeDefiniteFieldsFromModel(self):
        expected_fields = [
            'serial_number', 'title', 'description', 'id', 'lesson_type',
            'is_completed', 'children',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': String,
            'lesson_type': String,
            'is_completed': Boolean,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(field).__class__ == NonNull for field in [
                'serial_number', 'title', 'description',
            ]
        ])

        expected_children = List
        real_children = real_fields.pop('children')

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)
        self.assertIsInstance(real_children, expected_children)

    def test_When_SendQueryWithOutAuthenticate_Should_ErrorHasNotPermission(
            self):
        response = self.client.execute(
            """
            query GetLessonsByCourse ($courseId: String!){
                lessonsByCourse (courseId: $courseId){
                    isCompleted
                }
            }
            """,
            variables={
                'courseId': self.course_id,
            },
        )

        expected_data = {
            'data': {
                'lessonsByCourse': [
                    {
                        'isCompleted': None,
                    },
                    {
                        'isCompleted': None,
                    },
                ],
            },
            'errors': [
                {
                    'locations': [{'column': 21, 'line': 4, }, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': ['lessonsByCourse', 0, 'isCompleted', ],
                },
                {
                    'locations': [{'column': 21, 'line': 4, }, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': ['lessonsByCourse', 1, 'isCompleted', ],
                },
            ],
        }
        real_data = response.formatted

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithChildrenNotAuth_Should_ErrorHasNotPermission(
            self):
        response = self.client.execute(
            """
            query GetLessonsByCourse ($courseId: String!){
                lessonsByCourse (courseId: $courseId){
                    children {
                        isCompleted
                    }
                }
            }
            """,
            variables={
                'courseId': self.course_id,
            },
        )

        expected_data = {
            'data': {
                'lessonsByCourse': [
                    {
                        'children': [
                            {
                                'isCompleted': None,
                            },
                        ],
                    },
                    {
                        'children': [],
                    },
                ],
            },
            'errors': [
                {
                    'locations': [{'column': 25, 'line': 5, }, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': [
                        'lessonsByCourse', 0, 'children', 0, 'isCompleted',
                    ],
                },
            ],
        }
        real_data = response.formatted

        self.maxDiff = None

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithNotValidCourseID_Should_ErrorNotValidCourseID(
            self):
        response = self.gql_client.execute(
            """
            query GetLessonsByCourse ($courseId: String!){
                lessonsByCourse (courseId: $courseId){
                    id
                }
            }
            """,
            variables={
                'courseId': 'OjE=',
            },
            context=self.context,
        )

        expected_data = {
            'data': {
                'lessonsByCourse': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'courseId: This is not global Id.',
                    'path': ['lessonsByCourse', ],
                },
            ],
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithParentLessons_Should_ReturnWithOutErrors(self):
        response = self.gql_client.execute(
            """
            query GetLessonsByCourse ($courseId: String!){
                lessonsByCourse (courseId: $courseId){
                    id
                }
            }
            """,
            variables={
                'courseId': self.course_id,
            },
            context=self.context,
        )

        expected_data = {
            'data': {
                'lessonsByCourse': [
                    {
                        'id': 'TGVzc29uVHlwZTox',
                    },
                    {
                        'id': 'TGVzc29uVHlwZToy',
                    },
                ],
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithLessonTypeAndCompete_Should_ReturnWithOutErrors(
            self):
        response = self.gql_client.execute(
            """
            query GetLessonsByCourse ($courseId: String!){
                lessonsByCourse (courseId: $courseId){
                    id
                    lessonType
                    isCompleted
                }
            }
            """,
            variables={
                'courseId': self.course_id,
            },
            context=self.context,
        )

        expected_data = {
            'data': {
                'lessonsByCourse': [
                    {
                        'id': 'TGVzc29uVHlwZTox',
                        'lessonType': 'Тема',
                        'isCompleted': True,
                    },
                    {
                        'id': 'TGVzc29uVHlwZToy',
                        'lessonType': 'Тема',
                        'isCompleted': False,
                    },
                ],
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithChildrenLessons_Should_ReturnWithOutErrors(
            self):
        response = self.gql_client.execute(
            """
            query GetLessonsByCourse ($courseId: String!){
                lessonsByCourse (courseId: $courseId){
                    id
                    children {
                        id
                    }
                }
            }
            """,
            variables={
                'courseId': self.course_id,
            },
            context=self.context,
        )

        expected_data = {
            'data': {
                'lessonsByCourse': [
                    {
                        'id': 'TGVzc29uVHlwZTox',
                        'children': [
                            {
                                'id': 'TGVzc29uVHlwZToz',
                            },
                        ],
                    },
                    {
                        'id': 'TGVzc29uVHlwZToy',
                        'children': [],
                    },
                ],
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryOnProgressLessonsWithOutContext_Should_Errors(
            self):
        response = self.client.execute(
            """
            query GetLessonsByCourse ($courseId: String!){
                lessonsWithProgress (courseId: $courseId){
                    id
                }
            }
            """,
            variables={
                'courseId': self.course_id,
            },
        )

        expected_data = {
            'data': {
                'lessonsWithProgress': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': ['lessonsWithProgress', ],
                },
            ],
        }
        real_data = response.formatted

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryOnProgressLessonsWithNotValidCourseID_Should_Errors(
            self):
        response = self.gql_client.execute(
            """
            query GetLessonsByCourse ($courseId: String!){
                lessonsWithProgress (courseId: $courseId){
                    id
                }
            }
            """,
            variables={
                'courseId': 'OjE=',
            },
            context=self.context,
        )

        expected_data = {
            'data': {
                'lessonsWithProgress': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'courseId: This is not global Id.',
                    'path': ['lessonsWithProgress', ],
                },
            ],
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryOnProgressLessonsWithNotFoundCourseID_Should_Errors(
            self):
        response = self.gql_client.execute(
            """
            query GetLessonsByCourse ($courseId: String!){
                lessonsWithProgress (courseId: $courseId){
                    id
                }
            }
            """,
            variables={
                'courseId': 'Q291cnNlVHlwZToy',
            },
            context=self.context,
        )

        expected_data = {
            'data': {
                'lessonsWithProgress': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'You don`t have access to this course.',
                    'path': ['lessonsWithProgress', ],
                },
            ],
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryOnProgressLessons_Should_ReturnDataWithOutErrors(
            self):
        response = self.gql_client.execute(
            """
            query GetLessonsByCourse ($courseId: String!){
                lessonsWithProgress (courseId: $courseId){
                    id
                    isCompleted
                }
            }
            """,
            variables={
                'courseId': 'Q291cnNlVHlwZTox',
            },
            context=self.context,
        )

        expected_data = {
            'data': {
                'lessonsWithProgress': [
                    {
                        'id': 'TGVzc29uVHlwZTox',
                        'isCompleted': True,
                    },
                    {
                        'id': 'TGVzc29uVHlwZToy',
                        'isCompleted': False,
                    },
                ],
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
