from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import (BigAutoField, BooleanField, CharField,
                              DateTimeField, DecimalField, ForeignKey,
                              ImageField, IntegerField, ManyToManyField,
                              ManyToOneRel, OneToOneRel, PositiveIntegerField,
                              PositiveSmallIntegerField)
from django.test import TestCase
from django.utils import timezone

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.LearningFormat import LearningFormat


class CourseModelTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Course

        user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        cls.teacher = Teacher.objects.create(**{
            'user': user,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        cls.data = {
            'teacher': cls.teacher,
            'title': 'q' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        }

        cls.date_format = '%H-%M %d-%m-%Y'

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'course_body', 'statistic', 'discounts', 'user_courses', 'lessons',
            'payments', 'id', 'teacher', 'category', 'title', 'price',
            'count_lectures', 'count_independents', 'count_listeners',
            'duration', 'learning_format', 'preview', 'short_description',
            'avg_rating', 'created_at', 'is_published', 'listeners',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'course_body': OneToOneRel,
            'statistic': OneToOneRel,
            'discounts': ManyToOneRel,
            'user_courses': ManyToOneRel,
            'payments': ManyToOneRel,
            'lessons': ManyToOneRel,
            'id': BigAutoField,
            'teacher': ForeignKey,
            'title': CharField,
            'price': DecimalField,
            'avg_rating': DecimalField,
            'count_lectures': PositiveSmallIntegerField,
            'count_independents': PositiveSmallIntegerField,
            'count_listeners': PositiveSmallIntegerField,
            'duration': PositiveIntegerField,
            'learning_format': IntegerField,
            'category': ForeignKey,
            'preview': ImageField,
            'short_description': CharField,
            'created_at': DateTimeField,
            'is_published': BooleanField,
            'listeners': ManyToManyField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'id': '',
            'category': 'Course category.',
            'teacher': 'The teacher who leads the course.',
            'title': 'Course name.',
            'price': 'Course price.',
            'preview': 'Course picture.',
            'short_description': (
                'A few words about the course, shown on the course icon.'
            ),
            'avg_rating': (
                'Average rating based on comments, calculated automatically.'
            ),
            'count_independents': (
                'Count independents in course, calculated automatically.'
            ),
            'count_lectures': (
                'Count lectures in course, calculated automatically.'
            ),
            'count_listeners': (
                'Count listeners in course, calculated automatically.'
            ),
            'created_at': 'Course creation time.',
            'is_published': 'Course is published.',
            'listeners': 'All students of the course.',
            'course_body': '',
            'discounts': '',
            'duration': '',
            'learning_format': '',
            'lessons': '',
            'payments': '',
            'statistic': '',
            'user_courses': '',
        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreateCourseWithOutData_Should_ErrorBlankField(self):
        course = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            course.save()

        expected_raise = {
            'teacher': [
                'This field cannot be blank.',
            ],
            'title': [
                'This field cannot be blank.',
            ],
            'price': [
                'This field cannot be null.',
            ],
            'learning_format': [
                'This field cannot be null.',
            ],
            'category': [
                'This field cannot be blank.',
            ],
            'preview': [
                'This field cannot be blank.',
            ],
            'short_description': [
                'This field cannot be blank.',
            ],
        }
        real_raise = _raise.exception.message_dict

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
                'Ensure this value has at most 128 characters (it has 130).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_PriceAndDiscountDigitsGreaterThan7_Should_ErrorMaxDigits(
            self):
        data = self.data
        data.update({
            'price': f'{"1" * 7}.0',
        })

        course = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            course.save()

        expected_raise = {
            'price': [
                'Ensure that there are no more than 7 digits in total.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_PriceAndDiscountDecPlaceGreaterThan2_Should_ErrorMaxDecPlace(
            self):
        data = self.data
        data.update({
            'price': f'0.{"1" * 3}',
        })

        course = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            course.save()

        expected_raise = {
            'price': [
                'Ensure that there are no more than 2 decimal places.',
            ],
        }
        real_raise = _raise.exception.message_dict

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
                'Ensure this value has at most 255 characters (it has 256).',
            ],
        }
        real_raise = _raise.exception.message_dict

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

    def test_When_SaveCourse_Should_CreateUpdateTeacherCeleryTask(self):
        data = self.data

        course = self.tested_class(**data)
        course.save()

        course_stat = course.statistic
        course_stat.count_five_rating = 1
        course_stat.save()

        self.teacher.refresh_from_db()

        expected_average_rating = 5
        real_average_rating = self.teacher.avg_rating

        self.assertEqual(expected_average_rating, real_average_rating)

    def test_When_SaveCourse_Should_SetCreatedAtOnNow(self):
        data = self.data

        course = self.tested_class(**data)
        course.save()

        date_now = timezone.now()

        expected_str = date_now.strftime(self.date_format)
        real_str = course.created_at.strftime(self.date_format)

        self.assertEqual(expected_str, real_str)

    def test_When_CreateCourse_Should_CreateCourseStat(self):
        data = self.data

        course = self.tested_class(**data)
        expected_has = hasattr(course, 'statistic')

        course.save()
        real_has = hasattr(course, 'statistic')

        self.assertNotEqual(expected_has, real_has)
