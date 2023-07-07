from rest_framework.serializers import ModelSerializer
from snapshottest.django import TestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.Question import Question
from ...models.QuestionTypeChoices import QuestionTypeChoices
from ...serializers.QuestionSerializer import QuestionSerializer


class QuestionSerializerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = QuestionSerializer

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
            'lesson_type': LessonTypeChoices.TEST.value,
            'description': 'q' * 50,
        })

        Lesson.objects.create(**{
            'id': 2,
            'course': course,
            'title': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST.value,
            'description': 'q' * 50,
        })

        cls.question = Question.objects.create(**{
            'id': 1,
            'lesson': lesson,
            'body': 'q' * 50,
            'question_type': QuestionTypeChoices.RADIOBUTTON.value,
        })

        cls.data_with_one_answer = {
            'lesson': 1,
            'body': 'w' * 50,
            'question_type': QuestionTypeChoices.RADIOBUTTON.value,
            'answers': [
                {
                    'value': 'q' * 50,
                    'is_true': True,
                },
                {
                    'value': 'q' * 50,
                    'is_true': False,
                },
            ],
        }

        cls.data_with_many_answer = {
            'lesson': 1,
            'body': 'w' * 50,
            'question_type': QuestionTypeChoices.CHECKBOX.value,
        }

        cls.data_with_free_answer = {
            'lesson': 1,
            'body': 'w' * 50,
            'question_type': QuestionTypeChoices.FREE.value,
            'answers': [
                {
                    'value': 'q' * 50,
                    'is_true': True,
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
            'id', 'body', 'question_type', 'lesson',
        ]
        real_fields = list(self.tested_class().get_fields())

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificFormatForEachField(self):
        real_repr = repr(self.tested_class())

        self.assertMatchSnapshot(real_repr)

    def test_Should_DontOverrideSuperSaveMethod(self):
        expected_methods = [
            ModelSerializer.save,
            ModelSerializer.create,
            ModelSerializer.update,
        ]
        real_methods = [
            self.tested_class.save,
            self.tested_class.create,
            self.tested_class.update,
        ]

        self.assertEqual(expected_methods, real_methods)
