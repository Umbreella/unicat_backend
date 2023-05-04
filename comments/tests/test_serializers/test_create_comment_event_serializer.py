from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail, ValidationError

from events.models.Event import Event
from users.models import User

from ...models.Comment import Comment
from ...serializers.CreateCommentEventSerializer import \
    CreateCommentEventSerializer
from ...serializers.CreateCommentSerializer import CreateCommentSerializer


class CreateCommentEventSerializerTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CreateCommentEventSerializer

        user = User.objects.create(**{
            'email': 'q' * 10 + '@q.qq',
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

        cls.context = {
            'user': user,
        }

        cls.data = {
            'body': 'q' * 50,
            'commented_id': 'RXZlbnRUeXBlOjE=',
        }

        cls.date_format = '%H:%M %d-%m-%Y'

    def test_Should_InheritCreateCommentSerializer(self):
        expected_super_classes = (
            CreateCommentSerializer,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_When_CreateCommentWithNotValidCommentedId_Should_ReturnException(
            self):
        data = self.data
        data.update({
            'commented_id': 'OjE=',
        })
        context = self.context

        serializer = self.tested_class(data=data, context=context)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'commented_id': [
                ErrorDetail(**{
                    'string': 'This is not global Id.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_CreateCommentWithNotFoundCommentedID_Should_ReturnException(
            self):
        data = self.data
        data.update({
            'commented_id': 'RXZlbnRUeXBlOjU=',
        })
        context = self.context

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'commented_id': [
                ErrorDetail(**{
                    'string': 'Object with this id is not found',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

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
            'commented_type': 2,
            'count_like': 0,
            'id': 1,
            'rating': None
        }
        real_comment = created_comment

        expected_created_at = timezone.now().strftime(self.date_format)
        real_created_at = created_at.strftime(self.date_format)

        self.assertEqual(expected_comment, real_comment)
        self.assertEqual(expected_created_at, real_created_at)
