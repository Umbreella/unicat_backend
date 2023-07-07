import inspect
import os.path
from unittest import TestCase


class CountFileTestCase(TestCase):
    def test_Should_TestsForEachModule(self):
        exclude_dirs = (
            '__pycache__', 'migrations', 'tests', 'templates',
        )

        dir_tests, _ = os.path.split(inspect.getfile(self.__class__))
        dir_app, _ = os.path.split(dir_tests)

        tested_dirs = {}
        for file in os.scandir(dir_tests):
            if file.is_dir() and file.name not in exclude_dirs:
                key = file.name.replace('test_', '')
                value = len([
                    f for f in os.scandir(file.path) if f.is_file()
                ])

                tested_dirs.update({key: value, })

        code_dirs = {}
        for file in os.scandir(dir_app):
            if file.is_dir() and file.name not in exclude_dirs:
                key = file.name
                value = len([
                    f for f in os.scandir(file.path) if f.is_file()
                ])

                code_dirs.update({key: value, })

        expected_dirs = code_dirs
        real_dirs = tested_dirs

        self.assertEqual(expected_dirs, real_dirs)
