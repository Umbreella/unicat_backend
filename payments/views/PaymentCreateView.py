from decimal import Decimal

from django.utils import timezone
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from stripe.api_resources.payment_intent import PaymentIntent

from ..models.Payment import Payment
from ..serializers.PaymentCourseSerializer import PaymentCourseSerializer


class PaymentCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentCourseSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        course = serializer.course
        price = course.price

        discount = course.discounts.filter(**{
            'start_date__lte': timezone.now(),
            'end_date__gte': timezone.now(),
        }).first()

        if discount:
            price *= Decimal((100 - discount.percent) / 100)

        payment_intent = PaymentIntent.create(**{
            'amount': int(price * 100),
            'currency': 'rub',
        })

        Payment.objects.create(**{
            'id': payment_intent['id'],
            'amount': payment_intent['amount'] / 100,
            'user': user,
            'course': course,
        })

        response_data = {
            'amount': payment_intent['amount'],
            'clientSecret': payment_intent['client_secret'],
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
