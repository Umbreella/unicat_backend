from copy import copy
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Comment import Comment
from ...models.CommentedType import CommentedType


class CategoryModelTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Comment

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

        cls.course = Course.objects.create(**{
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

        cls.course_comment_data = {
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedType.COURSE.value,
            'commented_id': 1,
            'rating': 5,
        }

        cls.news_comment_data = {
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedType.NEWS.value,
            'commented_id': 1,
        }

        cls.event_comment_data = {
            'author': user,
            'body': 'q' * 50,
            'commented_type': CommentedType.EVENT.value,
            'commented_id': 1,
        }

        cls.date_format = "%H:%M %d-%m-%Y"

    def test_Should_IndexesInCommentTable(self):
        expected_indexes = [
            ['commented_type', 'commented_id'],
        ]
        real_indexes = [index.fields for index in
                        self.tested_class._meta.indexes]

        self.assertEqual(expected_indexes, real_indexes)

    def test_When_CreateCommentWithOutData_Should_ErrorBlankField(self):
        comment = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            comment.save()

        expected_raise = {
            'author': ['This field cannot be null.'],
            'body': ['This field cannot be blank.'],
            'commented_id': ['This field cannot be null.'],
            'commented_type': ['This field cannot be blank.'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_CommentedTypeIsRandomText_Should_ErrorIsNotValidChoice(self):
        data = self.news_comment_data
        data.update({
            'commented_type': 'q' * 8,
        })

        comment = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            comment.save()

        expected_raise = {
            'commented_type': ['Value \'qqqqqqqq\' is not a valid choice.'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_SetOnlyBlankData_Should_SetOtherDataWithDefaultValue(self):
        data = self.news_comment_data

        comment = self.tested_class(**data)
        comment.save()

        expected_created_at = timezone.now().strftime(self.date_format)
        real_created_at = comment.created_at.strftime(self.date_format)

        expected_count_like = 0
        real_count_like = comment.count_like

        expected_rating = None
        real_rating = comment.rating

        self.assertEqual(expected_created_at, real_created_at)
        self.assertEqual(expected_count_like, real_count_like)
        self.assertEqual(expected_rating, real_rating)

    def test_When_AllDataIsValid_Should_SaveNewAndReturnTitleAsStr(self):
        data = self.news_comment_data

        comment = self.tested_class(**data)
        comment.save()

        expected_str = f'{comment.created_at} | {comment.commented_type}:' \
                       f'{comment.commented_id} - {comment.author}'
        real_str = str(comment)

        self.assertEqual(expected_str, real_str)

    def test_When_CreateCourseCommentWithRating5_Should_UpdateCourseStat(self):
        data = self.course_comment_data

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_save = copy(course_stat.__dict__)
        course_stat_before_save.update({
            'avg_rating': Decimal('5.0'),
            'count_comments': 1,
            'count_five_rating': 1,
        })

        comment = self.tested_class(**data)
        comment.save()

        course_stat.refresh_from_db()
        course_stat_after_save = course_stat.__dict__

        expected_course_stat = course_stat_before_save
        real_course_stat = course_stat_after_save

        self.assertEqual(expected_course_stat, real_course_stat)

    def test_When_DeleteCourseCommentWithRating5_Should_UpdateCourseStat(self):
        data = self.course_comment_data

        comment = self.tested_class(**data)
        comment.save()

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_delete = copy(course_stat.__dict__)
        course_stat_before_delete.update({
            'avg_rating': Decimal('0.0'),
            'count_comments': 0,
            'count_five_rating': 0,
        })

        comment.delete()

        course_stat.refresh_from_db()
        course_stat_after_delete = course_stat.__dict__

        expected_course_stat = course_stat_before_delete
        real_course_stat = course_stat_after_delete

        self.assertEqual(expected_course_stat, real_course_stat)

    def test_When_CreateCourseCommentWithRating4_Should_UpdateCourseStat(self):
        data = self.course_comment_data
        data.update({
            'rating': 4,
        })

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_save = copy(course_stat.__dict__)
        course_stat_before_save.update({
            'avg_rating': Decimal('4.0'),
            'count_comments': 1,
            'count_four_rating': 1,
        })

        comment = self.tested_class(**data)
        comment.save()

        course_stat.refresh_from_db()
        course_stat_after_save = course_stat.__dict__

        expected_course_stat = course_stat_before_save
        real_course_stat = course_stat_after_save

        self.assertEqual(expected_course_stat, real_course_stat)

    def test_When_DeleteCourseCommentWithRating4_Should_UpdateCourseStat(self):
        data = self.course_comment_data
        data.update({
            'rating': 4,
        })

        comment = self.tested_class(**data)
        comment.save()

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_delete = copy(course_stat.__dict__)
        course_stat_before_delete.update({
            'avg_rating': Decimal('0.0'),
            'count_comments': 0,
            'count_four_rating': 0,
        })

        comment.delete()

        course_stat.refresh_from_db()
        course_stat_after_delete = course_stat.__dict__

        expected_course_stat = course_stat_before_delete
        real_course_stat = course_stat_after_delete

        self.assertEqual(expected_course_stat, real_course_stat)

    def test_When_CreateCourseCommentWithRating3_Should_UpdateCourseStat(self):
        data = self.course_comment_data
        data.update({
            'rating': 3,
        })

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_save = copy(course_stat.__dict__)
        course_stat_before_save.update({
            'avg_rating': Decimal('3.0'),
            'count_comments': 1,
            'count_three_rating': 1,
        })

        comment = self.tested_class(**data)
        comment.save()

        course_stat.refresh_from_db()
        course_stat_after_save = course_stat.__dict__

        expected_course_stat = course_stat_before_save
        real_course_stat = course_stat_after_save

        self.assertEqual(expected_course_stat, real_course_stat)

    def test_When_DeleteCourseCommentWithRating3_Should_UpdateCourseStat(self):
        data = self.course_comment_data
        data.update({
            'rating': 3,
        })

        comment = self.tested_class(**data)
        comment.save()

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_delete = copy(course_stat.__dict__)
        course_stat_before_delete.update({
            'avg_rating': Decimal('0.0'),
            'count_comments': 0,
            'count_three_rating': 0,
        })

        comment.delete()

        course_stat.refresh_from_db()
        course_stat_after_delete = course_stat.__dict__

        expected_course_stat = course_stat_before_delete
        real_course_stat = course_stat_after_delete

        self.assertEqual(expected_course_stat, real_course_stat)

    def test_When_CreateCourseCommentWithRating2_Should_UpdateCourseStat(self):
        data = self.course_comment_data
        data.update({
            'rating': 2,
        })

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_save = copy(course_stat.__dict__)
        course_stat_before_save.update({
            'avg_rating': Decimal('2.0'),
            'count_comments': 1,
            'count_two_rating': 1,
        })

        comment = self.tested_class(**data)
        comment.save()

        course_stat.refresh_from_db()
        course_stat_after_save = course_stat.__dict__

        expected_course_stat = course_stat_before_save
        real_course_stat = course_stat_after_save

        self.assertEqual(expected_course_stat, real_course_stat)

    def test_When_DeleteCourseCommentWithRating2_Should_UpdateCourseStat(self):
        data = self.course_comment_data
        data.update({
            'rating': 2,
        })

        comment = self.tested_class(**data)
        comment.save()

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_delete = copy(course_stat.__dict__)
        course_stat_before_delete.update({
            'avg_rating': Decimal('0.0'),
            'count_comments': 0,
            'count_two_rating': 0,
        })

        comment.delete()

        course_stat.refresh_from_db()
        course_stat_after_delete = course_stat.__dict__

        expected_course_stat = course_stat_before_delete
        real_course_stat = course_stat_after_delete

        self.assertEqual(expected_course_stat, real_course_stat)

    def test_When_CreateCourseCommentWithRating1_Should_UpdateCourseStat(self):
        data = self.course_comment_data
        data.update({
            'rating': 1,
        })

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_save = copy(course_stat.__dict__)
        course_stat_before_save.update({
            'avg_rating': Decimal('1.0'),
            'count_comments': 1,
            'count_one_rating': 1,
        })

        comment = self.tested_class(**data)
        comment.save()

        course_stat.refresh_from_db()
        course_stat_after_save = course_stat.__dict__

        expected_course_stat = course_stat_before_save
        real_course_stat = course_stat_after_save

        self.assertEqual(expected_course_stat, real_course_stat)

    def test_When_DeleteCourseCommentWithRating1_Should_UpdateCourseStat(self):
        data = self.course_comment_data
        data.update({
            'rating': 1,
        })

        comment = self.tested_class(**data)
        comment.save()

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_delete = copy(course_stat.__dict__)
        course_stat_before_delete.update({
            'avg_rating': Decimal('0.0'),
            'count_comments': 0,
            'count_one_rating': 0,
        })

        comment.delete()

        course_stat.refresh_from_db()
        course_stat_after_delete = course_stat.__dict__

        expected_course_stat = course_stat_before_delete
        real_course_stat = course_stat_after_delete

        self.assertEqual(expected_course_stat, real_course_stat)

    def test_When_UpdateCourseComment_Should_OnlyUpdateComment(self):
        data = self.course_comment_data

        comment = self.tested_class(**data)
        comment.save()

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_update = copy(course_stat.__dict__)

        comment.rating = 3
        comment.save()

        course_stat.refresh_from_db()
        course_stat_after_update = course_stat.__dict__

        expected_course_stat = course_stat_before_update
        real_course_stat = course_stat_after_update

        self.assertEqual(expected_course_stat, real_course_stat)

    def test_When_CreateNewsComment_Should_OnlySaveComment(self):
        data = self.news_comment_data

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_save = copy(course_stat.__dict__)

        comment = self.tested_class(**data)
        comment.save()

        course_stat.refresh_from_db()
        course_stat_after_save = course_stat.__dict__

        expected_course_stat = course_stat_before_save
        real_course_stat = course_stat_after_save

        self.assertEqual(expected_course_stat, real_course_stat)

    def test_When_DeleteNewsComment_Should_OnlyDeleteComment(self):
        data = self.news_comment_data

        comment = self.tested_class(**data)
        comment.save()

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_delete = copy(course_stat.__dict__)

        comment.delete()

        course_stat.refresh_from_db()
        course_stat_after_delete = course_stat.__dict__

        expected_course_stat = course_stat_before_delete
        real_course_stat = course_stat_after_delete

        self.assertEqual(expected_course_stat, real_course_stat)

    def test_When_CreateEventComment_Should_OnlySaveComment(self):
        data = self.event_comment_data

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_save = copy(course_stat.__dict__)

        comment = self.tested_class(**data)
        comment.save()

        course_stat.refresh_from_db()
        course_stat_after_save = course_stat.__dict__

        expected_course_stat = course_stat_before_save
        real_course_stat = course_stat_after_save

        self.assertEqual(expected_course_stat, real_course_stat)

    def test_When_DeleteEventComment_Should_OnlyDeleteComment(self):
        data = self.event_comment_data

        comment = self.tested_class(**data)
        comment.save()

        course_stat = self.course.statistic

        course_stat.refresh_from_db()
        course_stat_before_delete = copy(course_stat.__dict__)

        comment.delete()

        course_stat.refresh_from_db()
        course_stat_after_delete = course_stat.__dict__

        expected_course_stat = course_stat_before_delete
        real_course_stat = course_stat_after_delete

        self.assertEqual(expected_course_stat, real_course_stat)
