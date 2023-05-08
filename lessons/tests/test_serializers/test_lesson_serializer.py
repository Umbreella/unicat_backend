from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.serializers import ModelSerializer
from snapshottest.django import TestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonBody import LessonBody
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.Question import Question
from ...models.QuestionTypeChoices import QuestionTypeChoices
from ...serializers.LessonSerializer import LessonSerializer


class LessonSerializerTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LessonSerializer

        user = User.objects.create_superuser(**{
            'email': 'test@email.com',
            'password': 'password',
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

        Course.objects.create(**{
            'id': 2,
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

        lesson_theme = Lesson.objects.create(**{
            'id': 1,
            'course': course,
            'title': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME.value,
            'description': 'q' * 50,
        })

        cls.data_lesson_theme = {
            'course': course.id,
            'title': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEME.value,
            'description': 'q' * 50,
            'parent': None,
        }

        cls.data_lesson_theory = {
            'course': course.id,
            'title': 'q' * 50,
            'lesson_type': LessonTypeChoices.THEORY.value,
            'description': 'q' * 50,
            'body': 'q' * 50,
            'parent': lesson_theme.id,
        }

        cls.data_lesson_test = {
            'course': course.id,
            'title': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST.value,
            'description': 'q' * 50,
            'parent': lesson_theme.id,
            'questions': [
                {
                    'body': 'w' * 50,
                    'question_type': QuestionTypeChoices.FREE.value,
                    'answers': [
                        {
                            'value': 'q' * 50,
                            'is_true': True,
                        },
                    ],
                },
            ],
        }

    def test_Should_InheritModelSerializer(self):
        expected_super_classes = (
            ModelSerializer,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_IncludeDefiniteFieldsFromCommentModel(self):
        expected_fields = [
            'id', 'course', 'title', 'lesson_type', 'description', 'body',
            'parent', 'questions',
        ]
        real_fields = list(self.tested_class().get_fields())

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificFormatForEachField(self):
        real_repr = repr(self.tested_class())

        self.assertMatchSnapshot(real_repr)

    def test_Should_DontOverrideSuperSaveMethod(self):
        expected_method = ModelSerializer.save
        real_method = self.tested_class.save

        self.assertEqual(expected_method, real_method)

    def test_Should_OverrideSuperCreateMethod(self):
        expected_method = ModelSerializer.create
        real_method = self.tested_class.create

        self.assertNotEqual(expected_method, real_method)

    def test_Should_OverrideSuperUpdateMethod(self):
        expected_method = ModelSerializer.update
        real_method = self.tested_class.update

        self.assertNotEqual(expected_method, real_method)

    def test_When_LessonIsTheoryAndBodyIsEmpty_Should_ErrorLessonTypeArgs(
            self):
        data = self.data_lesson_theory
        del data['body']

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'body': [
                ErrorDetail(**{
                    'string': 'Required field for this lesson_type.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_LessonIsThemeAndParentIsNotNone_Should_ErrorLessonTypeArgs(
            self):
        data = self.data_lesson_theme
        data.update({
            'parent': 1,
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'parent': [
                ErrorDetail(**{
                    'string': 'Theme can`t have parent_lesson.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_LessonIsTheme_Should_CreateLessonTheme(self):
        data = self.data_lesson_theme

        serializer = self.tested_class(data=data)
        serializer.is_valid()
        serializer.save()

        expected_data = {
            'id': 2,
            'course': 1,
            'title': 'q' * 50,
            'lesson_type': 1,
            'description': 'q' * 50,
            'body': None,
            'parent': None,
            'questions': [],
        }
        real_data = serializer.data

        self.assertEqual(expected_data, real_data)

    def test_When_LessonIsTheory_Should_CreateLessonTheoryAndLessonBody(self):
        data = self.data_lesson_theory

        serializer = self.tested_class(data=data)
        serializer.is_valid()
        serializer.save()

        expected_data = {
            'id': 2,
            'course': 1,
            'title': 'q' * 50,
            'lesson_type': 2,
            'description': 'q' * 50,
            'body': 'q' * 50,
            'parent': 1,
            'questions': [],
        }
        real_data = serializer.data

        expected_count_lesson_body = 1
        real_count_lesson_body = len(LessonBody.objects.all())

        self.assertEqual(expected_data, real_data)
        self.assertEqual(expected_count_lesson_body, real_count_lesson_body)

    def test_When_LessonIsTest_Should_CreateLessonTestAndQuestions(self):
        data = self.data_lesson_test

        serializer = self.tested_class(data=data)
        serializer.is_valid()
        serializer.save()

        expected_data = {
            'id': 2,
            'course': 1,
            'title': 'q' * 50,
            'lesson_type': 3,
            'description': 'q' * 50,
            'body': None,
            'parent': 1,
            'questions': [
                {
                    'id': 1,
                    'body': 'w' * 50,
                    'question_type': 3,
                    'lesson': 2,
                },
            ],
        }
        real_data = serializer.data

        expected_count_questions = 1
        real_count_questions = len(Question.objects.all())

        self.assertEqual(expected_data, real_data)
        self.assertEqual(expected_count_questions, real_count_questions)

    def test_When_UpdateLessonTheme_Should_UpdateLessonTheme(self):
        save_data = self.data_lesson_theme

        save_serializer = self.tested_class(data=save_data)
        save_serializer.is_valid()
        save_serializer.save()

        data = save_data
        data.update({
            'course': 2,
            'title': 'w' * 50,
        })

        instance = save_serializer.instance
        serializer = self.tested_class(data=data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        expected_data = {
            'id': 2,
            'course': 1,
            'title': 'w' * 50,
            'lesson_type': 1,
            'description': 'q' * 50,
            'body': None,
            'parent': None,
            'questions': [],
        }
        real_data = serializer.data

        self.assertEqual(expected_data, real_data)

    def test_When_UpdateLessonTheory_Should_UpdateLessonBody(self):
        save_data = self.data_lesson_theory

        save_serializer = self.tested_class(data=save_data)
        save_serializer.is_valid()
        save_serializer.save()

        data = save_data
        data.update({
            'course': 2,
            'description': 'w' * 50,
            'body': 'w' * 50,
        })

        instance = save_serializer.instance
        serializer = self.tested_class(data=data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        expected_data = {
            'id': 2,
            'course': 1,
            'title': 'q' * 50,
            'lesson_type': 2,
            'description': 'w' * 50,
            'body': 'w' * 50,
            'parent': 1,
            'questions': [],
        }
        real_data = serializer.data

        self.assertEqual(expected_data, real_data)

    def test_When_UpdateLessonTest_Should_DontChangeQuestions(self):
        save_data = self.data_lesson_test

        save_serializer = self.tested_class(data=save_data)
        save_serializer.is_valid()
        save_serializer.save()

        data = save_data
        data.update({
            'course': 2,
            'title': 'w' * 50,
            'questions': [
                {
                    'body': 'w' * 50,
                    'question_type': QuestionTypeChoices.FREE.value,
                    'answers': [
                        {
                            'value': 'q' * 50,
                            'is_true': True,
                        },
                    ],
                },
                {
                    'body': 'w' * 50,
                    'question_type': QuestionTypeChoices.FREE.value,
                    'answers': [
                        {
                            'value': 'q' * 50,
                            'is_true': True,
                        },
                    ],
                },
            ],
        })

        instance = save_serializer.instance
        serializer = self.tested_class(data=data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        expected_data = {
            'id': 2,
            'course': 1,
            'title': 'w' * 50,
            'lesson_type': 3,
            'description': 'q' * 50,
            'body': None,
            'parent': 1,
            'questions': [
                {
                    'id': 1,
                    'body': 'w' * 50,
                    'question_type': 3,
                    'lesson': 2,
                },
            ],
        }
        real_data = serializer.data

        self.assertEqual(expected_data, real_data)
