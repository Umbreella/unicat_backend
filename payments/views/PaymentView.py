from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF

from ..filtersets.PaymentFilterBackend import PaymentFilterBackend
from ..models.Payment import Payment
from ..serializers.PaymentSerializer import PaymentSerializer


class PaymentView(ModelViewSet):
    queryset = Payment.objects.select_related(
        'user', 'course'
    ).filter(is_success=True).all()
    permission_classes = (DjModelPermForDRF,)
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, PaymentFilterBackend,
                       SearchFilter, OrderingFilter,)
    filterset_fields = ('user', 'course',)
    search_fields = ('course__title',)
    ordering_fields = '__all__'
    ordering = ('-created_at',)
