import tempfile
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import connections
from django.db.models import (BigAutoField, DateTimeField, ForeignKey,
                              IntegerField)
from django.test import TestCase
from django.utils import timezone
from django.utils.connection import ConnectionProxy

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.Discount import Discount
from ...models.LearningFormat import LearningFormat


class DiscountModelTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Discount

        temporary_img = tempfile.NamedTemporaryFile(suffix='.jpg').name

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
            'preview': temporary_img,
            'short_description': 'q' * 50,
        })

        cls.data = {
            'course': course,
            'percent': 10,
            'start_date': timezone.now() + timedelta(days=6),
            'end_date': timezone.now() + timedelta(days=9),
        }

        with ConnectionProxy(connections, 'master').cursor() as c:
            c.execute("""
            INSERT INTO courses_discount(
                percent,
                start_date,
                end_date,
                course_id
            )
            VALUES (5, '%s', '%s', 1);
            """ % (
                timezone.now() - timedelta(days=5),
                timezone.now() + timedelta(days=5),
            ))
            c.execute("""
            INSERT INTO courses_discount(
                percent,
                start_date,
                end_date,
                course_id
            )
            VALUES (10, '%s', '%s', 1);
            """ % (
                timezone.now() + timedelta(days=10),
                timezone.now() + timedelta(days=20),
            ))

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'id', 'course', 'percent', 'start_date', 'end_date',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'course': ForeignKey,
            'percent': IntegerField,
            'start_date': DateTimeField,
            'end_date': DateTimeField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_When_CreateDiscountWithOutData_Should_ErrorNullField(self):
        discount = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            discount.save()

        expected_raise = {
            'course': [
                'This field cannot be null.',
            ],
            'percent': [
                'This field cannot be null.',
            ],
            'start_date': [
                'This field cannot be null.',
            ],
            'end_date': [
                'This field cannot be null.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_PercentLessThan1_Should_ErrorMinValue(self):
        data = self.data
        data.update({
            'percent': 0,
        })

        discount = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            discount.save()

        expected_raise = {
            'percent': [
                'Ensure this value is greater than or equal to 1.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_PercentGreaterThan100_Should_ErrorMaxValue(self):
        data = self.data
        data.update({
            'percent': 101,
        })

        discount = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            discount.save()

        expected_raise = {
            'percent': [
                'Ensure this value is less than or equal to 100.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_DiscountStartToday_Should_ErrorDiscountCanStartOnlyTomorrow(
            self):
        data = self.data
        data.update({
            'start_date': timezone.now(),
        })

        discount = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            discount.save()

        expected_raise = {
            'start_date': [
                'Discount must start no earlier than tomorrow.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_StartDateAfterEndDate_Should_ErrorErroneousData(
            self):
        data = self.data
        data.update({
            'start_date': timezone.now() + timedelta(days=10),
        })

        discount = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            discount.save()

        expected_raise = {
            'start_date': [
                'Erroneous date values.',
            ],
            'end_date': [
                'Erroneous date values.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_StartDateInOtherDiscountPeriod_Should_ErrorManyDiscounts(
            self):
        data = self.data
        data.update({
            'start_date': timezone.now() + timedelta(days=3),
        })
        discount = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            discount.save()

        expected_raise = {
            '__all__': [
                'This course has other discounts for this interval.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_EndDateInOtherDiscountPeriod_Should_ErrorManyDiscounts(
            self):
        data = self.data
        data.update({
            'end_date': timezone.now() + timedelta(days=12),
        })
        discount = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            discount.save()

        expected_raise = {
            '__all__': [
                'This course has other discounts for this interval.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_IntervalInOtherDiscountPeriod_Should_ErrorManyDiscounts(
            self):
        data = self.data
        data.update({
            'start_date': timezone.now() + timedelta(days=3),
            'end_date': timezone.now() + timedelta(days=12),
        })
        discount = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            discount.save()

        expected_raise = {
            '__all__': [
                'This course has other discounts for this interval.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SaveDiscount(self):
        data = self.data

        discount = self.tested_class(**data)
        discount.save()

        expected_str = f'{discount.course} - {discount.percent}%'
        real_str = str(discount)

        self.assertEqual(expected_str, real_str)

    def test_When_AllDataIsValid_Should_UpdateDiscount(self):
        data = self.data

        discount = self.tested_class(**data)
        discount.save()

        new_start_date = timezone.now() + timedelta(days=7)

        discount.start_date = new_start_date
        discount.save()

        expected_start_date = new_start_date
        real_start_date = discount.start_date

        self.assertEqual(expected_start_date, real_start_date)
