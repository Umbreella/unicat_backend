from django.test import TestCase
from django_filters import OrderingFilter

from events.models.Event import Event
from events.models.New import New
from users.models import User

from ...filtersets.CommentFilterSet import CommentFilterSet
from ...models.Comment import Comment
from ...models.CommentedTypeChoices import CommentedTypeChoices


class CommentFilterSetTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CommentFilterSet

        user = User.objects.create(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
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
            'commented_type': CommentedTypeChoices.NEWS.value,
            'commented_id': 1,
        })

        Comment.objects.create(**{
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedTypeChoices.EVENT.value,
            'commented_id': 1,
        })

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'order_by',
        ]
        real_fields = list(self.tested_class.get_filters())

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'order_by': OrderingFilter,
        }
        real_fields = {
            key: value.__class__
            for key, value in self.tested_class.get_filters().items()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_When_OrderByCreated_Should_ReturnOrderedData(self):
        data = {
            'order_by': 'created_at',
        }
        base_queryset = Comment.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = list(base_queryset.order_by('created_at'))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_OrderByCreatedDesc_Should_ReturnOrderedData(self):
        data = {
            'order_by': '-created_at',
        }
        base_queryset = Comment.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = list(base_queryset.order_by('-created_at'))
        real_queryset = list(filtered_data.qs)

        self.assertEqual(expected_queryset, real_queryset)
