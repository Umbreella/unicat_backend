from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import (BigAutoField, DecimalField, OneToOneField,
                              PositiveIntegerField)
from django.test import TestCase

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.CourseStat import CourseStat
from ...models.LearningFormat import LearningFormat


class CourseStatTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CourseStat

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
            'id': 1,
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

        cls.course_stat = course.statistic

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'id', 'course', 'avg_rating', 'count_comments',
            'count_five_rating', 'count_four_rating', 'count_three_rating',
            'count_two_rating', 'count_one_rating',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'course': OneToOneField,
            'avg_rating': DecimalField,
            'count_comments': PositiveIntegerField,
            'count_five_rating': PositiveIntegerField,
            'count_four_rating': PositiveIntegerField,
            'count_three_rating': PositiveIntegerField,
            'count_two_rating': PositiveIntegerField,
            'count_one_rating': PositiveIntegerField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_When_CreateCourseStatWithOutData_Should_ErrorBlankField(self):
        course_stat = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            course_stat.save()

        expected_raise = {
            'course': [
                'This field cannot be null.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SaveCourseBodyAndReturnSubBody(self):
        course_stat = self.course_stat

        expected_dict = {
            'avg_rating': Decimal('0'),
            'count_comments': 0,
            'count_five_rating': 0,
            'count_four_rating': 0,
            'count_one_rating': 0,
            'count_three_rating': 0,
            'count_two_rating': 0,
            'course_id': 1,
            'id': 1,
        }
        real_dict = dict(course_stat)

        self.assertEqual(expected_dict, real_dict)

    def test_When_AddComment_Should_UpdateCountCommentsAndAvgRating(self):
        course_stat = self.course_stat

        course_stat.count_five_rating += 1
        course_stat.save()

        expected_dict = {
            'avg_rating': Decimal('5'),
            'count_comments': 1,
            'count_five_rating': 1,
            'count_four_rating': 0,
            'count_one_rating': 0,
            'count_three_rating': 0,
            'count_two_rating': 0,
            'course_id': 1,
            'id': 1,
        }
        real_dict = dict(course_stat)

        self.assertEqual(expected_dict, real_dict)

    def test_When_DeleteComment_Should_UpdateCountCommentsAndAvgRating(self):
        course_stat = self.course_stat

        course_stat.count_five_rating += 1
        course_stat.count_one_rating += 1
        course_stat.save()

        course_stat.count_one_rating -= 1
        course_stat.save()

        expected_dict_after_comment_delete = {
            'avg_rating': Decimal('5'),
            'count_comments': 1,
            'count_five_rating': 1,
            'count_four_rating': 0,
            'count_one_rating': 0,
            'count_three_rating': 0,
            'count_two_rating': 0,
            'course_id': 1,
            'id': 1,
        }
        real_dict_after_comment_delete = dict(course_stat)

        self.assertEqual(expected_dict_after_comment_delete,
                         real_dict_after_comment_delete)

    def test_When_AllDeleteComment_Should_UpdateCountCommentsAndAvgRating(
            self):
        course_stat = self.course_stat

        course_stat.count_five_rating += 1
        course_stat.save()

        course_stat.count_five_rating -= 1
        course_stat.save()

        expected_dict = {
            'avg_rating': Decimal('0'),
            'count_comments': 0,
            'count_five_rating': 0,
            'count_four_rating': 0,
            'count_one_rating': 0,
            'count_three_rating': 0,
            'count_two_rating': 0,
            'course_id': 1,
            'id': 1,
        }
        real_dict = dict(course_stat)

        self.assertEqual(expected_dict, real_dict)
