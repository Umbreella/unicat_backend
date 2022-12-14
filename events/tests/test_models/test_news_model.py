import tempfile
from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from users.models import User

from ...models.New import New


class NewsModelTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        temporary_img = tempfile.NamedTemporaryFile(suffix=".jpg").name

        user = User.objects.create(**{
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        cls.data = {
            'preview': temporary_img,
            'title': 'q' * 50,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
            'author': user,
            'created_at': '2001-01-01'
        }

    def test_When_CreateNewsWithOutData_Should_ErrorBlankField(self):
        news = New()

        with self.assertRaises(ValidationError) as _raise:
            news.save()

        expected_raise = {
            'preview': ['This field cannot be blank.'],
            'title': ['This field cannot be blank.'],
            'short_description': ['This field cannot be blank.'],
            'description': ['This field cannot be blank.'],
            'author': ['This field cannot be blank.'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataLengthGreaterThan255_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'title': 'q' * 275,
            'short_description': 'q' * 275,
        })

        news = New(**data)

        with self.assertRaises(ValidationError) as _raise:
            news.save()

        expected_raise = {
            'short_description': [
                'Ensure this value has at most 255 characters (it has 275).'],
            'title': [
                'Ensure this value has at most 255 characters (it has 275).'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SaveNewAndReturnTitleAsStr(self):
        data = self.data

        news = New(**data)
        news.save()

        expected_str = news.title
        real_str = str(news)

        self.assertEqual(expected_str, real_str)

    def test_When_DontSetCreatedAt_Should_SaveNewWithCreatedAtNow(self):
        data = self.data
        data.pop('created_at')

        news = New(**data)
        news.save()

        expected_created_at = news.created_at
        real_created_at = datetime.now().date()

        self.assertEqual(expected_created_at, real_created_at)
