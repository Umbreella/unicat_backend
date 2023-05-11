from django.urls import path

from .views.PaymentCreateView import PaymentCreateView
from .views.PaymentWebhookView import PaymentWebhookView

urlpatterns = [
    path('create/', PaymentCreateView.as_view(), name='payment_create'),
    path('webhook/', PaymentWebhookView.as_view(), name='payment_webhook'),
]
