from django.test import TestCase

from ..urls import urlpatterns


class CoursesUrlsTestCase(TestCase):
    databases = {'master', }

    def test_Should_AllUrlsWithSlash(self):
        all_urls_closed = all([
            str(url.pattern).endswith('/')
            if str(url.pattern) else True for url in urlpatterns
        ])

        self.assertTrue(all_urls_closed)
