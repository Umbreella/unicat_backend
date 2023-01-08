from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase
from django.utils import timezone

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.LearningFormat import LearningFormat


class CourseModelTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Course

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

        cls.data = {
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
        }

        cls.date_format = "%H-%M %d-%m-%Y"

    def test_When_CreateCourseWithOutData_Should_ErrorBlankField(self):
        course = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            course.save()

        expected_raise = {
            'teacher': ['This field cannot be blank.'],
            'title': ['This field cannot be blank.'],
            'price': ['This field cannot be null.'],
            'learning_format': ['This field cannot be blank.'],
            'category': ['This field cannot be blank.'],
            'preview': ['This field cannot be blank.'],
            'short_description': ['This field cannot be blank.'],
            'description': ['This field cannot be blank.'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_TitleLengthGreaterThan128_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'title': 'q' * 130
        })

        course = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            course.save()

        expected_raise = {
            'title': [
                'Ensure this value has at most 128 characters (it has 130).'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_PriceAndDiscountDigitsGreaterThan7_Should_ErrorMaxDigits(
            self):
        data = self.data
        data.update({
            'price': f'{"1" * 7}.0',
            'discount': f'{"1" * 7}.0',
        })

        course = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            course.save()

        expected_raise = {
            'price': [
                'Ensure that there are no more than 7 digits in total.'],
            'discount': [
                'Ensure that there are no more than 7 digits in total.'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_PriceAndDiscountDecPlaceGreaterThan2_Should_ErrorMaxDecPlace(
            self):
        data = self.data
        data.update({
            'price': f'0.{"1" * 3}',
            'discount': f'0.{"1" * 3}',
        })

        course = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            course.save()

        expected_raise = {
            'price': [
                'Ensure that there are no more than 2 decimal places.'],
            'discount': [
                'Ensure that there are no more than 2 decimal places.'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_ShortDescriptionLengthGreaterThan128_Should_ErrorMaxLength(
            self):
        data = self.data
        data.update({
            'short_description': 'q' * 256
        })

        course = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            course.save()

        expected_raise = {
            'short_description': [
                'Ensure this value has at most 255 characters (it has 256).'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_DeleteTeacherAndCategory_Should_SetNullValue(self):
        teacher_meta = self.tested_class._meta.get_field('teacher')
        category_meta = self.tested_class._meta.get_field('category')

        expected_delete_teacher = models.SET_NULL
        real_delete_teacher = teacher_meta.remote_field.on_delete

        expected_delete_category = models.SET_NULL
        real_delete_category = category_meta.remote_field.on_delete

        self.assertEqual(expected_delete_teacher, real_delete_teacher)
        self.assertEqual(expected_delete_category, real_delete_category)

    def test_When_AllDataIsValid_Should_SaveCourseAndReturnTitle(self):
        data = self.data

        course = self.tested_class(**data)
        course.save()

        expected_str = course.title
        real_str = str(course)

        self.assertEqual(expected_str, real_str)

    def test_When_SaveCourse_Should_SetCreatedByOnNow(self):
        data = self.data

        course = self.tested_class(**data)
        course.save()

        date_now = timezone.now()

        expected_str = date_now.strftime(self.date_format)
        real_str = course.created_at.strftime(self.date_format)

        self.assertEqual(expected_str, real_str)
