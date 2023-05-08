from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.serializers import ModelSerializer
from snapshottest.django import TestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.AnswerValue import AnswerValue
from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.Question import Question
from ...models.QuestionTypeChoices import QuestionTypeChoices
from ...serializers.QuestionSerializer import QuestionSerializer


class QuestionSerializerTestCase(TestCase):
    databases = {'master'}

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
            'discount': None,
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
            'answers': [
                {
                    'value': 'q' * 50,
                    'is_true': True,
                },
                {
                    'value': 'q' * 50,
                    'is_true': True,
                },
            ],
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
            'id', 'body', 'question_type', 'lesson', 'answers',
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

    def test_When_DataIsNotValid_Should_ErrorRequiredFields(
            self):
        data = self.data_with_one_answer
        del data['lesson']

        serializer = self.tested_class(data=data)
        serializer.is_valid(raise_exception=True)

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'lesson': [
                ErrorDetail(**{
                    'string': [
                        'This field cannot be null.',
                    ],
                    'code': 'null',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_QuestionWithOneTrueAnswer_Should_CreateQuestionAndAnswers(
            self):
        data = self.data_with_one_answer

        serializer = self.tested_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        expected_question = {
            'id': 2,
            'lesson_id': 1,
            'body': 'w' * 50,
            'question_type': 1,
        }
        real_question = dict(Question.objects.last())

        expected_answers = [
            {
                'id': 1,
                'question_id': 2,
                'value': 'q' * 50,
                'is_true': True,
            },
            {
                'id': 2,
                'question_id': 2,
                'value': 'q' * 50,
                'is_true': False,
            },
        ]
        real_answers = [dict(answer) for answer in AnswerValue.objects.all()]

        self.assertEqual(expected_question, real_question)
        self.assertEqual(expected_answers, real_answers)

    def test_When_QuestionWithManyTrueAnswers_Should_CreateQuestionAndAnswers(
            self):
        data = self.data_with_many_answer

        serializer = self.tested_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        expected_question = {
            'id': 2,
            'lesson_id': 1,
            'body': 'w' * 50,
            'question_type': 2,
        }
        real_question = dict(Question.objects.last())

        expected_answers = [
            {
                'id': 1,
                'question_id': 2,
                'value': 'q' * 50,
                'is_true': True,
            },
            {
                'id': 2,
                'question_id': 2,
                'value': 'q' * 50,
                'is_true': True,
            },
        ]
        real_answers = [dict(answer) for answer in AnswerValue.objects.all()]

        self.assertEqual(expected_question, real_question)
        self.assertEqual(expected_answers, real_answers)

    def test_When_QuestionWithOnlyOneTrueAnswer_Should_CreateQuestionAndAnswer(
            self):
        data = self.data_with_free_answer

        serializer = self.tested_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        expected_question = {
            'id': 2,
            'lesson_id': 1,
            'body': 'w' * 50,
            'question_type': 3,
        }
        real_question = dict(Question.objects.last())

        expected_answers = [
            {
                'id': 1,
                'question_id': 2,
                'value': 'q' * 50,
                'is_true': True,
            },
        ]
        real_answers = [dict(answer) for answer in AnswerValue.objects.all()]

        self.assertEqual(expected_question, real_question)
        self.assertEqual(expected_answers, real_answers)

    def test_When_QuestionWithOnlyOneTrueAnswerButAnswersMuch_Should_Error(
            self):
        data = self.data_with_free_answer
        data.update({
            'answers': [
                {
                    'value': 'q' * 50,
                    'is_true': True,
                },
                {
                    'value': 'q' * 50,
                    'is_true': True,
                },
            ],
        })

        serializer = self.tested_class(data=data)
        serializer.is_valid(raise_exception=True)

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'answers': [
                ErrorDetail(**{
                    'string': 'Much values for this question_type.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_UpdateQuestion_Should_DontChangeLessonAndAnswers(self):
        data = self.data_with_free_answer
        data.update({
            'lesson': 2,
        })

        serializer = self.tested_class(data=data, instance=self.question)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.question.refresh_from_db()

        expected_question = {
            'id': 1,
            'lesson': 1,
            'body': 'w' * 50,
            'question_type': 3,
        }
        real_question = serializer.data

        expected_count_answers = 0
        real_count_answers = len(AnswerValue.objects.all())

        self.assertEqual(expected_question, real_question)
        self.assertEqual(expected_count_answers, real_count_answers)
