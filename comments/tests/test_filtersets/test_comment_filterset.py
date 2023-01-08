from django.test import TestCase

from users.models import User

from ...filtersets.CommentFilterSet import CommentFilterSet
from ...models.Comment import Comment
from ...models.CommentedType import CommentedType


class CommentFilterSetTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CommentFilterSet

        user = User.objects.create(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        Comment.objects.create(**{
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedType.NEWS.value,
            'commented_id': 1,
        })

        Comment.objects.create(**{
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedType.EVENT.value,
            'commented_id': 2,
        })

    def test_Should_IncludeOrderByFilterName(self):
        dict_keys = dict(self.tested_class.get_filters()).keys()

        expected_filters = [
            'order_by',
        ]
        real_filters = [key for key in dict_keys]

        self.assertEqual(expected_filters, real_filters)

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
