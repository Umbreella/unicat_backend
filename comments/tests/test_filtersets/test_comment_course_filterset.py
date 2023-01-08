from django.test import TestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...filtersets.CommentCourseFilterSet import CommentCourseFilterSet
from ...models.Comment import Comment
from ...models.CommentedType import CommentedType


class CommentCourseFilterSetTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CommentCourseFilterSet

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
            'description': 'q' * 50,
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

        cls.comment = Comment.objects.create(**{
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedType.COURSE.value,
            'commented_id': 1,
            'rating': 5,
        })

        Comment.objects.create(**{
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedType.COURSE.value,
            'commented_id': 2,
            'rating': 5,
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
            'commented_id': 1,
        })

    def test_Should_SuperClassIsCommentFilterSetTest(self):
        super_classes = self.tested_class.__bases__

        expected_super_classes = [
            'CommentFilterSet',
        ]
        real_super_classes = [_super.__name__ for _super in super_classes]

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_IncludeOrderByFilterName(self):
        expected_filters = [
            'order_by', 'course_id',
        ]
        real_filters = list(self.tested_class.get_filters())

        self.assertEqual(expected_filters, real_filters)

    def test_Should_UseOrderByFromSuperClass(self):
        super_class = self.tested_class.__base__
        super_filters = dict(super_class.get_filters())

        tested_filters = dict(self.tested_class.get_filters())

        expected_order_by = super_filters['order_by']
        real_order_by = tested_filters['order_by']

        self.assertEqual(expected_order_by, real_order_by)

    def test_When_CourseIdIsValid_Should_ReturnFilteredCommentsByCourseId(
            self):
        data = {
            #   'OjE=' - ':1'
            'course_id': 'OjE=',
        }
        base_queryset = Comment.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = self.comment
        real_queryset = filtered_data.qs.first()

        self.assertEqual(expected_queryset, real_queryset)

    def test_When_CourseIdIsNotValid_Should_ReturnNullComments(self):
        data = {
            #   'OjM=' - ':3'
            'course_id': 'OjM=',
        }
        base_queryset = Comment.objects.all()

        filtered_data = self.tested_class(data=data, queryset=base_queryset)

        expected_queryset = None
        real_queryset = filtered_data.qs.first()

        self.assertEqual(expected_queryset, real_queryset)
