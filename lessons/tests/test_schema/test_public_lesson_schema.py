import graphene
from graphene import NonNull, Schema, String
from graphene.test import Client
from graphene_django.utils import GraphQLTestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...nodes.LessonTypeNode import LessonTypeNode
from ...schema.PublicLessonType import PublicLessonType


class PublicLessonTypeTestCase(GraphQLTestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = PublicLessonType
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

        lesson = Lesson.objects.create(**{
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
            'lesson_type': LessonTypeChoices.THEORY,
            'parent': lesson,
        })

        Lesson.objects.create(**{
            'id': 3,
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST,
            'parent': lesson,
        })

    def setUp(self):
        class PublicLessonQuery(graphene.ObjectType):
            public_lesson = LessonTypeNode.Field(PublicLessonType)

        schema = Schema(query=PublicLessonQuery)
        self.gql_client = Client(schema=schema)

    def test_Should_IncludeDefiniteDjangoModel(self):
        expected_model = self.model
        real_model = self.tested_class._meta.model

        self.assertEqual(expected_model, real_model)

    def test_Should_IncludeDefiniteInterfaces(self):
        expected_interfaces = [
            LessonTypeNode,
        ]
        real_interfaces = list(self.tested_class._meta.interfaces)

        self.assertEqual(expected_interfaces, real_interfaces)

    def test_Should_IncludeDefiniteFieldsFromModel(self):
        expected_fields = [
            'id', 'serial_number', 'title', 'description', 'lesson_type',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'lesson_type': String,
            'serial_number': String,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(field).__class__ == NonNull for field in [
                'id', 'title', 'description',
            ]
        ])

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)

    def test_When_SendQueryWithParentId_Should_ReturnDataWithOutErrors(self):
        response = self.gql_client.execute(
            """
            query {
                publicLesson (id: "UHVibGljTGVzc29uVHlwZTox") {
                    id
                    title
                    description
                    lessonType
                    serialNumber
                }
            }
            """
        )

        expected_response = {
            'data': {
                'publicLesson': {
                    'id': 'TGVzc29uVHlwZTox',
                    'title': 'q' * 50,
                    'description': 'q' * 50,
                    'lessonType': 'Тема',
                    'serialNumber': '1.',
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithChildrenId_Should_ReturnDataWithOutErrors(self):
        response = self.gql_client.execute(
            """
            query {
                publicLesson (id: "UHVibGljTGVzc29uVHlwZToy") {
                    id
                    title
                    description
                    lessonType
                    serialNumber
                }
            }
            """
        )

        expected_response = {
            'data': {
                'publicLesson': {
                    'id': 'TGVzc29uVHlwZToy',
                    'title': 'q' * 50,
                    'description': 'q' * 50,
                    'lessonType': 'Теория',
                    'serialNumber': '1.1.',
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithTestId_Should_ReturnDataWithOutErrors(self):
        response = self.gql_client.execute(
            """
            query {
                publicLesson (id: "UHVibGljTGVzc29uVHlwZToz") {
                    lessonType
                }
            }
            """
        )

        expected_response = {
            'data': {
                'publicLesson': {
                    'lessonType': 'Тест',
                },
            },
        }
        real_response = response

        self.assertEqual(expected_response, real_response)
