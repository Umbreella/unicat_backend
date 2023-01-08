from django.test import TestCase
from django.utils import timezone

from users.models import User

from ...models.Comment import Comment
from ...serializers.CommentEventSerializer import CommentEventSerializer


class CommentEventSerializerTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CommentEventSerializer

        user = User.objects.create(**{
            'email': 'q' * 10 + '@q.qq',
            'password': 'q' * 50,
        })

        cls.context = {
            'user': user,
        }

        cls.data = {
            'body': 'q' * 50,
            'commented_id': 'OjE=',
        }

        cls.date_format = "%H:%M %d-%m-%Y"

    def test_Should_SuperClassIsCommentSerializer(self):
        super_classes = self.tested_class.__bases__

        expected_super_classes = [
            'CommentSerializer',
        ]
        real_super_classes = [_super.__name__ for _super in super_classes]

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_When_CreateCommentWithRequiredData_Should_CreateWithEventType(
            self):
        data = self.data
        context = self.context

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()
        serializer.save()

        comment_id = serializer.data['id']
        created_comment = dict(Comment.objects.get(pk=comment_id))
        created_at = created_comment.pop('created_at')

        expected_comment = {
            'author_id': 1,
            'body': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq',
            'commented_id': 1,
            'commented_type': 'event',
            'count_like': 0,
            'id': 1,
            'rating': None
        }
        real_comment = created_comment

        expected_created_at = timezone.now().strftime(self.date_format)
        real_created_at = created_at.strftime(self.date_format)

        self.assertEqual(expected_comment, real_comment)
        self.assertEqual(expected_created_at, real_created_at)
