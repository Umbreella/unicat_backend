import json

from graphene import List
from graphene_django.utils import GraphQLTestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...schema.PublicLessonType import PublicLessonType
from ...schema.PublicParentLessonType import PublicParentLessonType


class PublicParentLessonTypeTestCase(GraphQLTestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = PublicParentLessonType
        cls.base_class = PublicLessonType

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
            'parent': lesson,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY,
            'serial_number': 2,
        })

        Lesson.objects.create(**{
            'id': 3,
            'course': course,
            'parent': lesson,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST,
            'serial_number': 1,
        })

    def test_Should_IncludeDefiniteDjangoModel(self):
        expected_model = self.base_class._meta.model
        real_model = self.tested_class._meta.model

        self.assertEqual(expected_model, real_model)

    def test_Should_IncludeDefiniteInterfaces(self):
        expected_interfaces = self.base_class._meta.interfaces
        real_interfaces = self.tested_class._meta.interfaces

        self.assertEqual(expected_interfaces, real_interfaces)

    def test_Should_IncludeDefiniteFieldsFromModel(self):
        expected_fields = [
            *list(self.base_class._meta.fields),
            'children',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            key: value.type
            for key, value in self.base_class._meta.fields.items()
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(f).__class__ == expected_fields.pop(f).__class__
            for f in [
                'id', 'title', 'description',
            ]
        ])

        expected_children = List
        real_children = real_fields.pop('children')

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)
        self.assertIsInstance(real_children, expected_children)

    def test_When_SendQueryWithNotValidCourseId_Should_ReturnErrors(self):
        response = self.query(
            """
            query {
                lessonsByCourse (courseId: "TGVzc29uVHlwZToz") {
                    id
                }
            }
            """,
        )

        expected_response = {
            'data': {
                'lessonsByCourse': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': 'courseId: not valid value.',
                    'path': ['lessonsByCourse', ],
                },
            ],
        }
        real_response = json.loads(response.content)

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithOutUser_Should_ReturnErrors(self):
        response = self.query(
            """
            query {
                lessonsByCourse (courseId: "Q291cnNlVHlwZTox") {
                    id
                    title
                    description
                    lessonType
                    serialNumber
                    children {
                        id
                        title
                        description
                        lessonType
                        serialNumber
                    }
                }
            }
            """,
        )

        expected_response = {
            'data': {
                'lessonsByCourse': [
                    {
                        'id': 'TGVzc29uVHlwZTox',
                        'title': 'q' * 50,
                        'description': 'q' * 50,
                        'lessonType': 'Тема',
                        'serialNumber': '1.',
                        'children': [
                            {
                                'id': 'TGVzc29uVHlwZToy',
                                'title': 'q' * 50,
                                'description': 'q' * 50,
                                'lessonType': 'Теория',
                                'serialNumber': '1.2.',
                            },
                        ],
                    },
                ],
            },
        }
        real_response = json.loads(response.content)

        self.assertEqual(expected_response, real_response)
