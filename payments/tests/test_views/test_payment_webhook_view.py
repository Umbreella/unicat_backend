from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer
from rest_framework.test import APITestCase
from stripe.error import SignatureVerificationError
from stripe.webhook import Webhook

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Payment import Payment
from ...views.PaymentWebhookView import PaymentWebhookView


class PaymentWebhookViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = PaymentWebhookView
        cls.serializer = Serializer
        cls.url = reverse('payment_webhook')

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
            'id': 1,
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

        cls.payment = Payment.objects.create(**{
            'id': 'q' * 27,
            'course': course,
            'user': user,
            'amount': 100.00,
        })

        def override_construct_event(*args, **kwargs):
            header = kwargs['sig_header']
            if not header:
                raise SignatureVerificationError(**{
                    'message': '',
                    'sig_header': '',
                })

            payload = str(kwargs['payload'], 'utf-8')
            if not payload:
                raise ValueError()

            event = type('event', (object,), {
                'type': header,
                'data': type('object', (object,), {
                    'object': {
                        'id': payload,
                    },
                }),
            })

            return event

        Webhook.construct_event = override_construct_event

    @classmethod
    def setUpClass(cls):
        cls.__construct_event = Webhook.construct_event
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        Webhook.construct_event = cls.__construct_event

    def test_Should_PermissionClassesIsAllowAny(self):
        expected_permission_classes = (
            AllowAny,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsLessonSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_When_GetMethodForPaymentWebhook_Should_ErrorWithStatus405(self):
        response = self.client.get(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethodForPaymentWebhook_Should_ErrorWithStatus405(self):
        response = self.client.put(self.url, data={})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethodForPaymentWebhook_Should_ErrorWithStatus405(self):
        response = self.client.patch(self.url, data={})

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethodForPaymentWebhook_Should_ErrorWithStatus405(
            self):
        response = self.client.delete(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethodWithValueError_Should_Status400(self):
        response = self.client.post(**{
            'path': self.url,
            'content_type': 'text/plain',
            'HTTP_STRIPE_SIGNATURE': 'payment_intent.succeeded',
        })

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_has_data = False
        real_has_data = hasattr(response, 'data')

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_has_data, real_has_data)

    def test_When_PostMethodWithSignatureError_Should_Status400(self):
        response = self.client.post(**{
            'path': self.url,
            'data': 'q' * 27,
            'content_type': 'text/plain',
        })

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_has_data = False
        real_has_data = hasattr(response, 'data')

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_has_data, real_has_data)

    def test_When_PostMethodWithNotValidEventType_Should_Status400(self):
        response = self.client.post(**{
            'path': self.url,
            'data': 'q' * 27,
            'content_type': 'text/plain',
            'HTTP_STRIPE_SIGNATURE': 'payment_intent.completed',
        })
        self.payment.refresh_from_db()

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_has_data = False
        real_has_data = hasattr(response, 'data')

        expected_is_success = False
        real_is_success = self.payment.is_success

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_has_data, real_has_data)
        self.assertEqual(expected_is_success, real_is_success)

    def test_When_PostMethodWithPaymentIDisNotFound_Should_Status400(self):
        response = self.client.post(**{
            'path': self.url,
            'data': 'q' * 20,
            'content_type': 'text/plain',
            'HTTP_STRIPE_SIGNATURE': 'payment_intent.succeeded',
        })
        self.payment.refresh_from_db()

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_has_data = False
        real_has_data = hasattr(response, 'data')

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_has_data, real_has_data)

    def test_When_PostMethodForPaymentWebhook_Should_ErrorWithStatus400(self):
        response = self.client.post(**{
            'path': self.url,
            'data': 'q' * 27,
            'content_type': 'text/plain',
            'HTTP_STRIPE_SIGNATURE': 'payment_intent.succeeded',
        })
        self.payment.refresh_from_db()

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_has_data = False
        real_has_data = hasattr(response, 'data')

        expected_is_success = True
        real_is_success = self.payment.is_success

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_has_data, real_has_data)
        self.assertEqual(expected_is_success, real_is_success)
