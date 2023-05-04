from django.test import TestCase
from django_filters import CharFilter, OrderingFilter

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from events.models.Event import Event
from events.models.New import New
from events.schema.EventType import EventType
from unicat.graphql.functions import get_id_from_value
from users.models import User
from users.models.Teacher import Teacher

from ...filtersets.CommentEventFilterSet import CommentEventFilterSet
from ...filtersets.CommentFilterSet import CommentFilterSet
from ...models.Comment import Comment
from ...models.CommentedTypeChoices import CommentedTypeChoices


class CommentEventFilterSetTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CommentEventFilterSet

        user = User.objects.create(**{
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

        Course.objects.create(**{
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

        Event.objects.create(**{
            'preview': 'temporary_img',
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'date': '2001-01-01',
            'start_time': '12:00:00',
            'end_time': '12:00:00',
            'place': 'q' * 50,
        })

        Event.objects.create(**{
            'preview': 'temporary_img',
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'date': '2001-01-01',
            'start_time': '12:00:00',
            'end_time': '12:00:00',
            'place': 'q' * 50,
        })

        New.objects.create(**{
            'preview': 'temporary_img',
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'author': user,
        })

        Comment.objects.create(**{
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedTypeChoices.COURSE.value,
            'commented_id': 1,
            'rating': 5,
        })

        Comment.objects.create(**{
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedTypeChoices.NEWS.value,
            'commented_id': 1,
        })

        cls.comment = Comment.objects.create(**{
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedTypeChoices.EVENT.value,
            'commented_id': 1,
        })

        Comment.objects.create(**{
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedTypeChoices.EVENT.value,
            'commented_id': 2,
        })

    def test_Should_SuperClassIsCommentFilterSetTest(self):
        expected_super_classes = (
            CommentFilterSet,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_IncludeRequiredFields(self):
        expected_filters = [
            'order_by', 'event_id',
        ]
        real_filters = list(self.tested_class.get_filters())

        self.assertEqual(expected_filters, real_filters)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'order_by': OrderingFilter,
            'event_id': CharFilter,
        }
        real_fields = {
            key: value.__class__
            for key, value in self.tested_class.get_filters().items()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_UseOrderByFromSuperClass(self):
        super_filters = CommentFilterSet.get_filters()
        tested_filters = self.tested_class.get_filters()

        expected_order_by = super_filters['order_by']
        real_order_by = tested_filters['order_by']

        self.assertEqual(expected_order_by, real_order_by)

    def test_When_EventIdIsNotValid_Should_ReturnException(self):
        data = {
            #   'OjM=' - ':3'
            'event_id': 'OjM=',
        }
        base_queryset = Comment.objects.all()

        with self.assertRaises(Exception) as expected_raise:
            get_id_from_value(EventType, data['event_id'])

        with self.assertRaises(Exception) as real_raise:
            self.tested_class(data=data, queryset=base_queryset).qs

        expected_exception = f'event_id: {expected_raise.exception}'
        real_exception = str(real_raise.exception)

        self.assertEqual(expected_exception, real_exception)

    def test_When_EventIdIsValid_Should_ReturnFilteredCommentsByEventId(self):
        data = {
            #   'RXZlbnRUeXBlOjE=' - 'EventType:1'
            'event_id': 'RXZlbnRUeXBlOjE=',
        }
        base_queryset = Comment.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = self.comment
        real_queryset = filtered_data.qs.first()

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_EventIdIsNotFound_Should_ReturnNullComments(self):
        data = {
            #   'RXZlbnRUeXBlOjU=' - 'EventType:5'
            'event_id': 'RXZlbnRUeXBlOjU=',
        }
        base_queryset = Comment.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = None
        real_queryset = filtered_data.qs.first()

        self.assertEqual(expected_queryset, real_queryset)
