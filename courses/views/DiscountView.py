from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ..models.Discount import Discount
from ..serializers.DiscountSerializer import DiscountSerializer


class DiscountView(ModelViewSet):
    queryset = Discount.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = DiscountSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('course',)
    ordering_fields = '__all__'
    ordering = ('id',)
