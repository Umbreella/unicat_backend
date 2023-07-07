from datetime import timedelta
from inspect import getmembers, isfunction

from django.test import TestCase
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

from ...graphql import functions


class FunctionsTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(**{
            'id': 1,
            'email': 'q' * 50 + 'q@q.ru',
            'password': 'q' * 50,
        })

    def test_Should_IncludeRequireDef(self):
        expected_def = [
            'allow_any', 'get_operation_name', 'get_timeout_seconds',
            'get_user_by_natural_key', 'get_user_model',
            'get_username_by_payload', 'jwt_decode',
        ]
        real_def = [
            func for func, _ in getmembers(functions, isfunction)
        ]

        expected_def_sorted = sorted(expected_def)
        real_def_sorted = sorted(real_def)

        self.assertEqual(expected_def_sorted, real_def_sorted)

    def test_When_UseGetTimeoutSecondWithNone_Should_ReturnNone(self):
        expected_result = None
        real_result = functions.get_timeout_seconds(None)

        self.assertEqual(expected_result, real_result)

    def test_When_UseGetTimeoutSecondWithFutureDateTime_Should_Seconds(
            self):
        future_time = timezone.now() + timedelta(seconds=10)

        expected_result = 10
        real_result = functions.get_timeout_seconds(future_time)

        self.assertEqual(expected_result, real_result)

    def test_When_UseJWTDecode_Should_ReturnDecodedPayload(self):
        token = RefreshToken.for_user(self.user).access_token
        result = functions.jwt_decode(str(token))

        expected_payload = {
            'token_type': 'access',
            'user_id': 1,
        }
        real_payload = {
            'token_type': result.get('token_type'),
            'user_id': result.get('user_id'),
        }

        self.assertEqual(expected_payload, real_payload)

    def test_When_UseGetUsernameByPayload_Should_ReturnUserId(self):
        payload = {
            'user_id': 1,
            'userid': 2,
        }

        expected_data = 1
        real_data = functions.get_username_by_payload(payload)

        self.assertEqual(expected_data, real_data)

    def test_When_UseGetUserByNaturalKeyWithNotValidData_Should_ReturnNone(
            self):
        expected_user = None
        real_user = functions.get_user_by_natural_key(2)

        self.assertEqual(expected_user, real_user)

    def test_When_UseGetUserByNaturalKeyWithValidData_Should_ReturnUser(
            self):
        expected_user = self.user
        real_user = functions.get_user_by_natural_key(1)

        self.assertEqual(expected_user, real_user)
