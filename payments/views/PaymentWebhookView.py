from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer
from stripe.error import SignatureVerificationError
from stripe.webhook import Webhook

from ..models.Payment import Payment


class PaymentWebhookView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = Serializer

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = Webhook.construct_event(**{
                'payload': payload,
                'sig_header': sig_header,
                'secret': endpoint_secret,
            })
        except ValueError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        except SignatureVerificationError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object

            try:
                active_payment = Payment.objects.using('master').get(**{
                    'id': payment_intent['id'],
                    'is_success': False,
                })
            except ObjectDoesNotExist:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            active_payment.is_success = True
            active_payment.save()

            return HttpResponse(status=status.HTTP_201_CREATED)

        return HttpResponse(status=status.HTTP_200_OK)
