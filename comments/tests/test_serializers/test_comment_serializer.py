from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail

from users.models import User

from ...models.Comment import Comment
from ...models.CommentedType import CommentedType
from ...serializers.CommentSerializer import CommentSerializer


class CommentSerializerTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CommentSerializer

        user = User.objects.create(**{
            'email': 'q' * 10 + '@q.qq',
            'password': 'q' * 50,
        })

        cls.comment = Comment(**{
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedType.NEWS.value,
            'commented_id': 1,
        })

        cls.date_format = "%d-%m-%Y"

    def test_Should_IncludeFieldsFromCommentModel(self):
        expected_fields = [
            'id', 'body', 'createdAt', 'countLike', 'commented_id', 'author'
        ]
        real_fields = list(self.tested_class().get_fields())

        self.assertEqual(expected_fields, real_fields)

    def test_When_EmptyData_Should_ErrorRequiredFields(self):
        data = {}

        serializer = self.tested_class(data=data)
        serializer.is_valid()

        expected_errors = {
            'body': [
                ErrorDetail(string='This field is required.', code='required')
            ],
            'commented_id': [
                ErrorDetail(string='This field is required.', code='required')
            ],
        }
        real_errors = serializer.errors

        self.assertEqual(expected_errors, real_errors)

    def test_When_EmptyFields_Should_ErrorBlankFields(self):
        data = {
            'body': '',
            'commented_id': '',
        }

        serializer = self.tested_class(data=data)
        serializer.is_valid()

        expected_errors = {
            'body': [
                ErrorDetail(string='This field may not be blank.',
                            code='blank')
            ],
            'commented_id': [
                ErrorDetail(string='This field may not be blank.',
                            code='blank')
            ],
        }
        real_errors = serializer.errors

        self.assertEqual(expected_errors, real_errors)

    def test_When_LenghtFieldsGreaterThan255_Should_ErrorMaxLength(self):
        data = {
            'body': 'q' * 50,
            'commented_id': 'q' * 256,
        }

        serializer = self.tested_class(data=data)
        serializer.is_valid()

        error_detail_str = 'Ensure this field has no more than 255 characters.'
        expected_errors = {
            'commented_id': [
                ErrorDetail(string=error_detail_str, code='max_length')
            ],
        }
        real_errors = serializer.errors

        self.assertEqual(expected_errors, real_errors)

    def test_When_AllDataIsValid_Should_(self):
        data = {
            'body': 'q' * 50,
            'commented_id': 'q' * 50,
        }

        serializer = self.tested_class(data=data, instance=self.comment)
        serializer.is_valid()

        created_at = timezone.now().strftime(self.date_format)

        expected_data = {
            'id': None,
            'body': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq',
            'createdAt': created_at,
            'countLike': 0,
            'author': 'qqqqqqqqqq@q.qq',
        }
        real_data = serializer.data

        self.assertEqual(expected_data, real_data)
