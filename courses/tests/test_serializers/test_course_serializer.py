from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.serializers import ModelSerializer
from snapshottest.django import TestCase

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.CourseBody import CourseBody
from ...serializers.CourseSerializer import CourseSerializer


class CourseSerializerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CourseSerializer

        first_user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        second_user = User.objects.create_user(**{
            'email': 'w' * 50 + '@q.qq',
            'password': 'w' * 50,
        })

        Teacher.objects.create(**{
            'user': first_user,
            'description': 'q' * 50,
        })

        Teacher.objects.create(**{
            'user': second_user,
            'description': 'q' * 50,
        })

        Category.objects.create(**{
            'title': 'q' * 50,
        })

        Category.objects.create(**{
            'title': 'w' * 50,
        })

        cls.data = {
            'teacher': 1,
            'title': 'q' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': 1,
            'category': 1,
            'short_description': 'q' * 50,
        }

    def test_Should_InheritModelSerializer(self):
        expected_super_classes = (
            ModelSerializer,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_IncludeDefiniteFieldsFromCommentModel(self):
        expected_fields = [
            'id', 'title', 'price', 'count_lectures', 'count_independents',
            'learning_format', 'category', 'teacher', 'preview',
            'short_description', 'body', 'is_published',
        ]
        real_fields = list(self.tested_class().get_fields())

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificFormatForEachField(self):
        real_repr = repr(self.tested_class())

        self.assertMatchSnapshot(real_repr)

    def test_Should_DontOverrideSuperMethods(self):
        expected_methods = [
            ModelSerializer.save,
        ]
        real_methods = [
            self.tested_class.save,
        ]

        self.assertEqual(expected_methods, real_methods)

    def test_Should_OverrideSuperMethodCreate(self):
        expected_method = ModelSerializer.create
        real_method = self.tested_class.create

        self.assertNotEqual(expected_method, real_method)

    def test_Should_OverrideSuperMethodUpdate(self):
        expected_method = ModelSerializer.update
        real_method = self.tested_class.update

        self.assertNotEqual(expected_method, real_method)

    def test_When_DataWithOutBody_Should_ErrorWithRequiredField(self):
        data = self.data

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'body': [
                ErrorDetail(string='This field is required.', code='required'),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_BodyIsEmpty_Should_ErrorEmptyFields(self):
        data = self.data
        data.update({
            'body': '',
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'body': [
                ErrorDetail(**{
                    'string': 'This field may not be blank.',
                    'code': 'blank',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataWithOutPreview_Should_ErrorWithRequiredField(self):
        data = self.data
        data.update({
            'body': 'q' * 50,
        })

        serializer = self.tested_class(data=data)
        serializer.is_valid()

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'preview': [
                ErrorDetail(**{
                    'string': 'This field cannot be blank.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_PreviewIsNotBase64_Should_ErrorNotValidPreviewValue(self):
        data = self.data
        data.update({
            'body': 'q' * 50,
            'preview': 'q' * 50,
        })

        serializer = self.tested_class(data=data)

        with self.assertRaises(ValidationError) as _raise:
            serializer.is_valid(raise_exception=True)

        expected_raise = {
            'preview': [
                ErrorDetail(**{
                    'string': 'Please upload a valid image.',
                    'code': 'invalid',
                }),
            ],
        }
        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)

    def test_When_PreviewIsBase64_Should_CreateNewCourse(self):
        data = self.data
        data.update({
            'body': 'q' * 50,
            'preview': (
                'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAIAAAACDbGyAAAAAXNSR0IArs4c6'
                'QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAANSURBVB'
                'hXY6AqYGAAAABQAAHTR4hjAAAAAElFTkSuQmCC'
            ),
        })

        serializer = self.tested_class(data=data)
        serializer.is_valid()
        serializer.save()

        expected_len = 1
        real_len = len(Course.objects.all())

        expected_body = 'q' * 50
        real_body = CourseBody.objects.first().body

        self.assertEqual(expected_len, real_len)
        self.assertEqual(expected_body, real_body)

    def test_When_DataForUpdate_Should_UpdateCourse(self):
        data = self.data
        data.update({
            'body': 'q' * 50,
            'preview': (
                'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAIAAAACDbGyAAAAAXNSR0IArs4c6'
                'QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAANSURBVB'
                'hXY6AqYGAAAABQAAHTR4hjAAAAAElFTkSuQmCC'
            ),
        })

        serializer = self.tested_class(data=data)
        serializer.is_valid()
        serializer.save()
        old_image = serializer.data['preview']

        update_serializer = self.tested_class(**{
            'instance': serializer.instance,
            'data': {
                'teacher': 2,
                'title': 'w' * 50,
                'price': 500.0,
                'count_lectures': 500,
                'count_independents': 500,
                'learning_format': 2,
                'category': 2,
                'short_description': 'w' * 50,
                'body': 'w' * 50,
                'preview': (
                    'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAAXNSR0IAr'
                    's4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAA'
                    'AYSURBVBhXY3wro/KfAQ0wQWkUQJEgAwMA4PUCNjunNCoAAAAASUVORK5'
                    'CYII='
                ),
            },
        })
        update_serializer.is_valid()
        update_serializer.save()

        expected_data = {
            'id': 1,
            'teacher': 2,
            'title': 'w' * 50,
            'price': '500.00',
            'count_lectures': 500,
            'count_independents': 500,
            'learning_format': 2,
            'category': 2,
            'short_description': 'w' * 50,
            'body': 'w' * 50,
            'is_published': False,
        }
        real_data = dict(update_serializer.data)

        new_image = real_data.pop('preview')

        self.assertEqual(expected_data, real_data)
        self.assertNotEqual(old_image, new_image)
