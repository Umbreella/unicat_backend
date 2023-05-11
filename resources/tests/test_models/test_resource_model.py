import inspect
import os
import shutil

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.utils import timezone

from ...models.Resource import Resource


@override_settings(
    MEDIA_ROOT=os.path.join(
        settings.BASE_DIR,
        os.path.normpath('resources/tests/test_models/files/'),
    ),
)
class ResourceModelTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Resource

        cls.data = {
            'name': 'q' * 50,
            'file': 'temporary.jpg',
        }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        module_dir = os.path.split(inspect.getfile(cls))[0]
        assert settings.MEDIA_ROOT.startswith(module_dir + '\\') is True, (
            'MEDIA_ROOT must be the path to a folder in the current directory.'
        )
        os.mkdir(settings.MEDIA_ROOT)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT)

    def setUp(self) -> None:
        self._path = os.path.join(settings.MEDIA_ROOT, 'temporary.jpg')
        with open(self._path, 'w'):
            pass

    def tearDown(self) -> None:
        if os.path.exists(self._path):
            os.remove(self._path)

    def test_When_CreateResourceWithOutData_Should_ErrorBlankField(self):
        resource = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            resource.save()

        expected_raise = {
            'name': [
                'This field cannot be blank.',
            ],
            'file': [
                'This field cannot be blank.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataGreaterThanMaxLength_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'name': 'q' * 256,
        })

        resource = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            resource.save()

        expected_raise = {
            'name': [
                'Ensure this value has at most 255 characters (it has 256).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_DataIsValid_Should_CreateResource(self):
        data = self.data

        resource = self.tested_class(**data)
        resource.save()

        expected_resource = Resource.objects.last()
        real_resource = resource

        date_format = '%d-%m-%Y %H-%M'
        expected_loaded_at = timezone.now().strftime(date_format)
        real_loaded_at = resource.loaded_at.strftime(date_format)

        self.assertEqual(expected_resource, real_resource)
        self.assertEqual(expected_loaded_at, real_loaded_at)

    def test_When_ResourceDelete_Should_DeleteFileFromDirectory(self):
        data = self.data

        resource = self.tested_class(**data)
        resource.save()
        resource.delete()

        expected_len_media_dir = 0
        real_len_media_dir = len(os.listdir(settings.MEDIA_ROOT))

        self.assertEqual(expected_len_media_dir, real_len_media_dir)
