from django.core.exceptions import ValidationError
from django.test import TestCase

from ...models.ShortLesson import ShortLesson


class ShortLessonModelTest(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.data = {
            'title': 'q' * 50,
            'description': 'q' * 50,
        }

    def test_When_CreateShortLessonWithOutData_Should_ErrorBlankFields(self):
        lesson = ShortLesson()

        with self.assertRaises(ValidationError) as _raise:
            lesson.save()

        expected_raise = {
            'description': ['This field cannot be blank.'],
            'title': ['This field cannot be blank.'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_LengthDataGreaterThan255_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'title': 'q' * 275,
            'description': 'q' * 275,
        })

        lesson = ShortLesson(**data)

        with self.assertRaises(ValidationError) as _raise:
            lesson.save()

        expected_raise = {
            'description': [
                'Ensure this value has at most 255 characters (it has 275).'],
            'title': [
                'Ensure this value has at most 255 characters (it has 275).'],
        }
        real_raise = dict(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_CreateParentShLesson_Should_SaveShLessonAndReturnCustomStr(
            self):
        data = self.data

        lesson = ShortLesson(**data)
        lesson.save()

        expected_str = f'{lesson.serial_number}. {lesson.title}'
        real_str = str(lesson)

        self.assertEqual(expected_str, real_str)

    def test_When_CreateChildShLesson_Should_SaveShLessonAndReturnIncludedStr(
            self):
        data = self.data

        parent_lesson = ShortLesson(**data)
        parent_lesson.save()

        child_lesson = ShortLesson(**data)
        child_lesson.parent_lesson = parent_lesson
        child_lesson.save()

        expected_str = f'{parent_lesson.serial_number}.' \
                       f'{child_lesson.serial_number}. ' \
                       f'{child_lesson.title}'
        real_str = str(child_lesson)

        self.assertEqual(expected_str, real_str)

    def test_When_ConvertShortLessonsToDict_Should_DelStateKey(self):
        data = self.data

        lesson = ShortLesson(**data)
        lesson.save()

        expected_keys = ['id', 'serial_number', 'title', 'description',
                         'parent_lesson_id', 'course_id']
        real_keys = list(dict(lesson).keys())

        self.assertEqual(expected_keys, real_keys)
