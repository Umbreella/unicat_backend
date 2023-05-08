from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ..models.AnswerValue import AnswerValue
from ..serializers.AnswerValueSerializer import AnswerValueSerializer


class AnswerValueView(ModelViewSet):
    queryset = AnswerValue.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = AnswerValueSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('question_id',)
    ordering = ('id',)
