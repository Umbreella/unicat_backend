from django.test import TestCase
from graphql_sync_dataloaders import SyncDataLoader

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...loaders.AnswerValueLoader import AnswerValueLoader, answer_value_loader
from ...models.AnswerValue import AnswerValue
from ...models.Lesson import Lesson
from ...models.LessonTypeChoices import LessonTypeChoices
from ...models.Question import Question
from ...models.QuestionTypeChoices import QuestionTypeChoices


class AnswerValueLoaderTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = AnswerValueLoader
        cls.batch_load_fn = answer_value_loader

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
            'course': course,
            'title': 'q' * 50,
            'description': 'q' * 50,
            'lesson_type': LessonTypeChoices.TEST,
        })

        question = Question.objects.create(**{
            'id': 1,
            'lesson': lesson,
            'body': 'q' * 50,
            'question_type': QuestionTypeChoices.RADIOBUTTON,
        })

        AnswerValue.objects.create(**{
            'id': 1,
            'question': question,
            'value': 'q' * 50,
        })

        AnswerValue.objects.create(**{
            'id': 2,
            'question': question,
            'value': '2' * 50,
        })

    def test_Should_InheritSyncDataLoader(self):
        expected_super_classes = (
            SyncDataLoader,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_OverrideSuperMethodInit(self):
        expected_method = SyncDataLoader.__init__
        real_method = self.tested_class.__init__

        self.assertNotEqual(expected_method, real_method)

    def test_Should_SetUpBatchLoadFN(self):
        expected_method = self.batch_load_fn
        real_method = self.tested_class()._batch_load_fn

        self.assertEqual(expected_method, real_method)

    def test_When_UseBatchLoadFN_Should_ReturnListOfQuerySet(self):
        keys = [1, 3, 5, ]

        expected_data = [
            [
                list(
                    AnswerValue.objects.filter(**{
                        'question_id__in': keys,
                    }).order_by('id')
                ),
                [], [],
            ],
            [
                list(
                    AnswerValue.objects.filter(**{
                        'question_id__in': keys,
                    }).order_by('-id')
                ),
                [], [],
            ],
        ]
        real_data = self.batch_load_fn(keys)

        self.assertIn(real_data, expected_data)
