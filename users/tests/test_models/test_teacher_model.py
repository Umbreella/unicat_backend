import tempfile

from django.core.exceptions import ValidationError
from django.test import TestCase

from ...models import User
from ...models.Teacher import Teacher


class UserModelTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        temporary_img = tempfile.NamedTemporaryFile(suffix=".jpg").name

        user = User.objects.create(**{
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
            'photo': temporary_img,
        })

        cls.data = {
            'user': user,
            'description': 'q' * 50,
            'average_rating': 1.0,
            'count_graduates': 1,
            'facebook': 'q' * 50,
            'twitter': 'q' * 50,
            'google_plus': 'q' * 50,
            'vk': 'q' * 50,
        }

    def test_When_CreateTeacherWithOutData_Should_ErrorBlankField(self):
        teacher = Teacher()

        with self.assertRaises(ValidationError) as _raise:
            teacher.save()

        expected_raise = {
            'description': ['This field cannot be blank.'],
            'user': ['This field cannot be null.'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_LengthDataGreaterThan255_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'description': 'q' * 275,
            'facebook': 'q' * 275,
            'twitter': 'q' * 275,
            'google_plus': 'q' * 275,
            'vk': 'q' * 275,
        })

        teacher = Teacher(**data)

        with self.assertRaises(ValidationError) as _raise:
            teacher.save()

        expected_raise = {
            'description': [
                'Ensure this value has at most 255 characters (it has 275).'],
            'facebook': [
                'Ensure this value has at most 255 characters (it has 275).'],
            'twitter': [
                'Ensure this value has at most 255 characters (it has 275).'],
            'google_plus': [
                'Ensure this value has at most 255 characters (it has 275).'],
            'vk': [
                'Ensure this value has at most 255 characters (it has 275).'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_TeacherWithOutLinks_Should_CreateTeacherAndReturnUser(self):
        data = self.data
        data.pop('facebook')
        data.pop('twitter')
        data.pop('google_plus')
        data.pop('vk')

        teacher = Teacher(**data)
        teacher.save()

        expected_str = str(teacher.user)
        real_str = str(teacher)

        self.assertEqual(expected_str, real_str)
