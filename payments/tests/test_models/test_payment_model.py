from django.core.exceptions import ValidationError
from django.db.models import (BooleanField, CharField, DateTimeField,
                              DecimalField, ForeignKey)
from django.test import TestCase
from django.utils import timezone

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from courses.models.UserCourse import UserCourse
from users.models import User
from users.models.Teacher import Teacher

from ...models.Payment import Payment


class PaymentModelTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Payment

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
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        cls.data = {
            'id': 'q' * 27,
            'user': user,
            'course': course,
            'amount': 100.12,
        }

        cls.date_format = '%H-%M %d-%m-%Y'

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'id', 'user', 'course', 'amount', 'created_at', 'is_success',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': CharField,
            'user': ForeignKey,
            'course': ForeignKey,
            'amount': DecimalField,
            'created_at': DateTimeField,
            'is_success': BooleanField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'id': 'Payment intent ID from StripeAPI.',
            'user': 'The user for whom the payment was created.',
            'course': 'The course for which the payment was created.',
            'amount': 'Amount of payment.',
            'created_at': 'Payment creation time.',
            'is_success': 'Payment status.',
        }
        real_help_text = {
            field.name: field.help_text
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreatePaymentWithOutData_Should_ErrorBlankField(self):
        payment = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            payment.save()

        expected_raise = {
            'id': [
                'This field cannot be blank.',
            ],
            'user': [
                'This field cannot be null.',
            ],
            'course': [
                'This field cannot be null.',
            ],
            'amount': [
                'This field cannot be null.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataGreaterThanMaxLength_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'id': 'q' * 30,
            'amount': '1' * 100,
        })

        payment = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            payment.save()

        expected_raise = {
            'id': [
                'Ensure this value has at most 27 characters (it has 30).',
            ],
            'amount': [
                'Ensure that there are no more than 9 digits in total.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataGreaterThanDecimalPlaces_Should_ErrorMaxDecimalPlaces(
            self):
        data = self.data
        data.update({
            'amount': '1.' + '0' * 3,
        })

        payment = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            payment.save()

        expected_raise = {
            'amount': [
                'Ensure that there are no more than 2 decimal places.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataIsValid_Should_CreatePayment(self):
        data = self.data

        payment = self.tested_class(**data)
        payment.save()

        expected_created_at = timezone.now().strftime(self.date_format)
        real_created_at = payment.created_at.strftime(self.date_format)

        expected_is_success = False
        real_is_success = payment.is_success

        self.assertEqual(expected_created_at, real_created_at)
        self.assertEqual(expected_is_success, real_is_success)

    def test_When_PaymentIsSuccessTrue_Should_CreateUserCourse(self):
        data = self.data

        payment = self.tested_class.objects.create(**data)
        payment.is_success = True
        payment.save()

        expected_len_user_course = 1
        real_len_user_course = len(UserCourse.objects.all())

        expected_data = {
            'course': payment.course_id,
            'user': payment.user_id,
        }
        real_data = UserCourse.objects.values(
            'course', 'user',
        ).last()

        self.assertEqual(expected_len_user_course, real_len_user_course)
        self.assertEqual(expected_data, real_data)
