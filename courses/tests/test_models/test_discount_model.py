import tempfile
from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.test import TestCase

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.Discount import Discount
from ...models.LearningFormat import LearningFormat


class DiscountModelTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        temporary_img = tempfile.NamedTemporaryFile(suffix=".jpg").name

        user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': user,
            'photo': temporary_img,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        course = Course.objects.create(**{
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
            'description': 'q' * 50,
        })

        cls.data = {
            'course': course,
            'new_price': 10.0,
            'start_date': '2001-01-01',
            'end_date': '2001-01-01',
        }

    def test_When_CreateDiscountWithOutData_Should_ErrorNullField(self):
        discount = Discount()

        with self.assertRaises(ValidationError) as _raise:
            discount.full_clean()

        expected_raise = {
            'course': ['This field cannot be null.'],
            'new_price': ['This field cannot be null.'],
            'start_date': ['This field cannot be null.'],
            'end_date': ['This field cannot be null.'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_NewPriceDigitsGreaterThan7_Should_ErrorMaxDigits(self):
        data = self.data
        data.update({
            'new_price': f'{"1" * 7}.0',
        })

        discount = Discount(**data)

        with self.assertRaises(ValidationError) as _raise:
            discount.full_clean()

        expected_raise = {
            'new_price': [
                'Ensure that there are no more than 7 digits in total.'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_NewPriceDecPlaceGreaterThan2_Should_ErrorMaxDecPlace(self):
        data = self.data
        data.update({
            'new_price': f'0.{"1" * 3}',
        })

        discount = Discount(**data)

        with self.assertRaises(ValidationError) as _raise:
            discount.full_clean()

        expected_raise = {
            'new_price': [
                'Ensure that there are no more than 2 decimal places.'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SaveDiscountAndReturnCustomStr(self):
        data = self.data

        discount = Discount(**data)
        discount.full_clean()

        expected_str = f'{discount.course} - {discount.new_price} ' \
                       f'(before {discount.end_date})'
        real_str = str(discount)

        self.assertEqual(expected_str, real_str)

    def test_When_DiscountPriceGreaterThanBasePrice_Should_DontCreateDiscount(
            self):
        data = self.data
        data.update({
            'new_price': 111.0
        })

        discount = Discount(**data)
        discount.save()

        with self.assertRaises(ObjectDoesNotExist) as _raise:
            discount.refresh_from_db()

        expected_raise = type(_raise.exception)
        real_raise = type(Discount.DoesNotExist())

        self.assertEqual(expected_raise, real_raise)

    def test_When_StartDateGreaterThanEndDate_Should_DontCreateDiscount(self):
        data = self.data

        start_date_as_date = datetime.strptime(data['start_date'],
                                               '%Y-%m-%d').date()

        data.update({
            'start_date': (start_date_as_date +
                           timedelta(days=1)).strftime('%Y-%m-%d')
        })

        discount = Discount(**data)
        discount.save()

        with self.assertRaises(ObjectDoesNotExist) as _raise:
            discount.refresh_from_db()

        expected_raise = type(_raise.exception)
        real_raise = type(Discount.DoesNotExist())

        self.assertEqual(expected_raise, real_raise)

    def test_When_NewPriceGreaterThanCoursePrice_Should_DontUpdatePrice(self):
        data = self.data

        discount = Discount(**data)
        discount.save()

        discount.new_price = 111.0
        discount.save()

        discount.refresh_from_db()

        expected_new_price = data['new_price']
        real_new_price = discount.new_price

        self.assertEqual(expected_new_price, real_new_price)

    def test_When_NewStartDateGreaterThanEndDate_Should_DontUpdateDates(self):
        data = self.data

        discount = Discount(**data)
        discount.save()

        base_date = datetime.strptime(discount.end_date, '%Y-%m-%d').date()
        discount.start_date = (base_date +
                               timedelta(days=1)).strftime('%Y-%m-%d')
        discount.save()
        discount.refresh_from_db()

        expected_start_date = base_date
        real_start_date = discount.start_date

        self.assertEqual(expected_start_date, real_start_date)

    def test_When_NewEndDateLowerThanStartDate_Should_DontUpdateDates(self):
        data = self.data

        discount = Discount(**data)
        discount.save()

        base_date = datetime.strptime(discount.end_date, '%Y-%m-%d').date()
        discount.end_date = (base_date -
                             timedelta(days=1)).strftime('%Y-%m-%d')
        discount.save()
        discount.refresh_from_db()

        expected_end_date = base_date
        real_end_date = discount.end_date

        self.assertEqual(expected_end_date, real_end_date)
