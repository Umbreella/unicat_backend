from django.urls import path

from .views.PaymentCreateView import PaymentCreateView
from .views.PaymentView import PaymentView
from .views.PaymentWebhookView import PaymentWebhookView

urlpatterns = [
    path(**{
        'route': 'create/',
        'view': PaymentCreateView.as_view(),
        'name': 'payment_create',
    }),
    path(**{
        'route': 'webhook/',
        'view': PaymentWebhookView.as_view(),
        'name': 'payment_webhook',
    }),
    path(**{
        'route': '',
        'view': PaymentView.as_view({
            'get': 'list',
        }),
        'name': 'payment_list',
    }),
]
