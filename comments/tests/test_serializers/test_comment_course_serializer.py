from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Comment import Comment
from ...serializers.CommentCourseSerializer import CommentCourseSerializer


class CommentCourseSerializerTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CommentCourseSerializer

        user = User.objects.create(**{
            'email': 'q' * 10 + '@q.qq',
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
            'description': 'q' * 50,
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

    def test_When_RatingIsEmpty_Should_ErrorRequiredFields(self):
        data = self.data
        context = self.context

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()

        expected_errors = {
            'rating': [
                ErrorDetail(string='This field is required.', code='required')
            ]
        }
        real_errors = serializer.errors

        self.assertEqual(expected_errors, real_errors)

    def test_When_RatingLessThan1_Should_ErrorMaxValue(self):
        data = self.data
        data.update({
            'rating': 0,
        })
        context = self.context

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()

        expected_errors = {
            'rating': [
                ErrorDetail(
                    string='Ensure this value is greater than or equal to 1.',
                    code='min_value')
            ]
        }
        real_errors = serializer.errors

        self.assertEqual(expected_errors, real_errors)

    def test_When_RatingGreaterThan5_Should_ErrorMaxValue(self):
        data = self.data
        data.update({
            'rating': 6,
        })
        context = self.context

        serializer = self.tested_class(data=data, context=context)
        serializer.is_valid()

        expected_errors = {
            'rating': [
                ErrorDetail(
                    string='Ensure this value is less than or equal to 5.',
                    code='max_value')
            ]
        }
        real_errors = serializer.errors

        self.assertEqual(expected_errors, real_errors)

    def test_When_CreateCommentWithRequiredData_Should_CreateWithCourseType(
            self):
        data = self.data
        data.update({
            'rating': 5,
        })
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
            'commented_type': 'course',
            'count_like': 0,
            'id': 1,
            'rating': 5,
        }
        real_comment = created_comment

        expected_created_at = timezone.now().strftime(self.date_format)
        real_created_at = created_at.strftime(self.date_format)

        self.assertEqual(expected_comment, real_comment)
        self.assertEqual(expected_created_at, real_created_at)
