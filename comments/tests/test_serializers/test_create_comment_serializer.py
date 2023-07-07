from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.fields import CharField, DateTimeField, IntegerField

from users.models import User

from ...models.Comment import Comment
from ...models.CommentedTypeChoices import CommentedTypeChoices
from ...serializers.CreateCommentSerializer import CreateCommentSerializer


class CreateCommentSerializerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CreateCommentSerializer

        user = User.objects.create(**{
            'email': 'q' * 10 + '@q.qq',
            'password': 'q' * 50,
        })

        cls.comment = Comment(**{
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedTypeChoices.NEWS.value,
            'commented_id': 1,
        })

        cls.date_format = '%d-%m-%Y'

    def test_Should_IncludeDefiniteFieldsFromCommentModel(self):
        expected_fields = [
            'id', 'body', 'createdAt', 'commented_id', 'author'
        ]
        real_fields = list(self.tested_class().get_fields())

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificFormatForEachField(self):
        expected_fields = {
            'id': IntegerField,
            'body': CharField,
            'createdAt': DateTimeField,
            'commented_id': CharField,
            'author': CharField,
        }
        real_fields = {
            key: value.__class__
            for key, value in self.tested_class().get_fields().items()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_When_EmptyData_Should_ErrorRequiredFields(self):
        data = {}

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_errors = {
            'body': [
                ErrorDetail(**{
                    'string': 'This field is required.',
                    'code': 'required',
                }),
            ],
            'commented_id': [
                ErrorDetail(**{
                    'string': 'This field is required.',
                    'code': 'required',
                }),
            ],
        }
        real_errors = _raise.exception.detail

        self.assertEqual(expected_errors, real_errors)

    def test_When_EmptyFields_Should_ErrorBlankFields(self):
        data = {
            'body': '',
            'commented_id': '',
        }

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_errors = {
            'body': [
                ErrorDetail(**{
                    'string': 'This field may not be blank.',
                    'code': 'blank',
                }),
            ],
            'commented_id': [
                ErrorDetail(**{
                    'string': 'This field may not be blank.',
                    'code': 'blank',
                }),
            ],
        }
        real_errors = _raise.exception.detail

        self.assertEqual(expected_errors, real_errors)

    def test_When_LengthFieldsGreaterThan255_Should_ErrorMaxLength(self):
        data = {
            'body': 'q' * 50,
            'commented_id': 'q' * 65,
        }

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_errors = {
            'commented_id': [
                ErrorDetail(**{
                    'string': 'Ensure this field has no more than 64 '
                              'characters.',
                    'code': 'max_length',
                }),
            ],
        }
        real_errors = _raise.exception.detail

        self.assertEqual(expected_errors, real_errors)

    def test_When_AllDataIsValid_Should_DontRaiseException(self):
        data = {
            'body': 'q' * 50,
            'commented_id': 'q' * 50,
        }

        serializer = self.tested_class(data=data, instance=self.comment)
        serializer.is_valid()

        expected_data = {
            'id': None,
            'body': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq',
            'createdAt': timezone.now().strftime(self.date_format),
            'author': 'qqqqqqqqqq@q.qq',
        }
        real_data = serializer.data

        self.assertEqual(expected_data, real_data)
