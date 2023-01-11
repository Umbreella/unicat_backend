import json
from http.cookies import SimpleCookie

from django.test import override_settings
from django.urls import path, reverse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.test import APITestCase, URLPatternsTestCase

from ...middleware.CookiesMiddleware import CookiesMiddleware

http_methods = [
    'POST', 'PUT', 'PATCH',
]


@api_view(http_methods)
@parser_classes((JSONParser,))
def ResponseFromRequestView(request):
    return Response({
        'data': request.data,
        'cookies': request.COOKIES,
    })


@override_settings(
    MIDDLEWARE=[
        'users.middleware.CookiesMiddleware.CookiesMiddleware',
    ]
)
class CookiesMiddlewareTestCase(APITestCase, URLPatternsTestCase):
    databases = {'master'}

    urlpatterns = [
        path('test', ResponseFromRequestView, name='test'),
        path('token_refresh', ResponseFromRequestView, name='token_refresh'),
        path('token_destroy', ResponseFromRequestView, name='token_destroy'),
    ]

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CookiesMiddleware

        cls.requests = {
            'POST': cls.client_class().post,
            'PUT': cls.client_class().put,
            'PATCH': cls.client_class().patch,
        }

        not_valid_cookies = SimpleCookie({
            'name': 'w' * 10,
        })
        cls.not_valid_cookies = {key: value.value for key, value in
                                 not_valid_cookies.items()}

        valid_cookies = SimpleCookie({
            'refresh': 'w' * 10,
        })
        cls.valid_cookies = {key: value.value for key, value in
                             valid_cookies.items()}

        client_with_not_valid_cookies = cls.client_class()
        client_with_not_valid_cookies.cookies = not_valid_cookies
        cls.requests_with_not_valid_cookies = {
            'POST': client_with_not_valid_cookies.post,
            'PUT': client_with_not_valid_cookies.put,
            'PATCH': client_with_not_valid_cookies.patch,
        }

        client_with_valid_cookies = cls.client_class()
        client_with_valid_cookies.cookies = valid_cookies
        cls.requests_with_valid_cookies = {
            'POST': client_with_valid_cookies.post,
            'PUT': client_with_valid_cookies.put,
            'PATCH': client_with_valid_cookies.patch,
        }

        cls.data = {
            'refresh': 'q' * 10,
        }
        cls.data_json_parsed = json.dumps(cls.data)
        cls.content_type = 'application/json'

    def test_When_UseInitMethod_Should_SetPropertyGetResponse(self):
        response = 'response'
        middleware = self.tested_class(response)

        expected_get_response = response
        real_get_response = middleware.get_response

        self.assertEqual(expected_get_response, real_get_response)

    def test_When_WriteRequestOnNotValidPathWithOutCookies_Should_DoNothing(
            self):
        url = reverse('test')
        asserts = []

        for http_method in http_methods:
            def_for_method = self.requests[http_method]
            response = def_for_method(path=url, data=self.data_json_parsed,
                                      content_type=self.content_type)

            expected_get_response = {
                'data': self.data,
                'cookies': {},
            }
            real_get_response = response.data

            asserts += [expected_get_response == real_get_response]

        expected_asserts = True
        real_asserts = all(asserts)

        self.assertEqual(expected_asserts, real_asserts)

    def test_When_WriteRequestOnNotValidPathWithNotValidCookies_Should_DoNoth(
            self):
        url = reverse('test')
        asserts = []

        for http_method in http_methods:
            def_for_method = self.requests_with_not_valid_cookies[http_method]
            response = def_for_method(path=url, data=self.data_json_parsed,
                                      content_type=self.content_type)

            expected_get_response = {
                'data': self.data,
                'cookies': self.not_valid_cookies,
            }
            real_get_response = response.data

            asserts += [expected_get_response == real_get_response]

        expected_asserts = True
        real_asserts = all(asserts)

        self.assertEqual(expected_asserts, real_asserts)

    def test_When_WriteRequestOnNotValidPathWithValidCookies_Should_DoNothing(
            self):
        url = reverse('test')
        asserts = []

        for http_method in http_methods:
            def_for_method = self.requests_with_valid_cookies[http_method]
            response = def_for_method(path=url, data=self.data_json_parsed,
                                      content_type=self.content_type)

            expected_get_response = {
                'data': self.data,
                'cookies': self.valid_cookies,
            }
            real_get_response = response.data

            asserts += [expected_get_response == real_get_response]

        expected_asserts = True
        real_asserts = all(asserts)

        self.assertEqual(expected_asserts, real_asserts)

    def test_When_WriteRequestOnValidPathWithOutCookies_Should_DoNothing(self):
        urls = [reverse('token_refresh'), reverse('token_destroy')]
        asserts = []

        for url in urls:
            for http_method in http_methods:
                def_for_method = self.requests[http_method]
                response = def_for_method(path=url, data=self.data_json_parsed,
                                          content_type=self.content_type)

                expected_get_response = {
                    'data': self.data,
                    'cookies': {},
                }
                real_get_response = response.data

                asserts += [expected_get_response == real_get_response]

        expected_asserts = True
        real_asserts = all(asserts)

        self.assertEqual(expected_asserts, real_asserts)

    def test_When_WriteRequestOnValidPathWithNotValidCookies_Should_DoNothing(
            self):
        urls = [reverse('token_refresh'), reverse('token_destroy')]
        asserts = []

        for url in urls:
            for method in http_methods:
                def_for_method = self.requests_with_not_valid_cookies[method]
                response = def_for_method(path=url, data=self.data_json_parsed,
                                          content_type=self.content_type)

                expected_get_response = {
                    'data': self.data,
                    'cookies': self.not_valid_cookies,
                }
                real_get_response = response.data

                asserts += [expected_get_response == real_get_response]

        expected_all_asserts = True
        real_all_asserts = all(asserts)

        self.assertEqual(expected_all_asserts, real_all_asserts)

    def test_When_NotPostRequestOnValidPathWithValidCookies_Should_DoNothing(
            self):
        urls = [reverse('token_refresh'), reverse('token_destroy')]
        asserts = []

        for url in urls:
            for method in http_methods:
                if method == 'POST':
                    continue

                def_for_method = self.requests_with_valid_cookies[method]
                response = def_for_method(path=url, data=self.data_json_parsed,
                                          content_type=self.content_type)

                expected_get_response = {
                    'data': self.data,
                    'cookies': self.valid_cookies,
                }
                real_get_response = response.data

                asserts += [expected_get_response == real_get_response]

        expected_all_asserts = True
        real_all_asserts = all(asserts)

        self.assertEqual(expected_all_asserts, real_all_asserts)

    def test_When_PostRequestOnValidPathWithValidCookies_Should_DoNothing(
            self):
        urls = [reverse('token_refresh'), reverse('token_destroy')]
        asserts = []

        for url in urls:
            def_for_method = self.requests_with_valid_cookies['POST']
            response = def_for_method(path=url, data=self.data_json_parsed,
                                      content_type=self.content_type)

            expected_get_response = {
                'data': self.valid_cookies,
                'cookies': self.valid_cookies,
            }
            real_get_response = response.data

            asserts += [expected_get_response == real_get_response]

        expected_all_asserts = True
        real_all_asserts = all(asserts)

        self.assertEqual(expected_all_asserts, real_all_asserts)
