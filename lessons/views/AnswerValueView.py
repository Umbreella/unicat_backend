from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF

from ..models.AnswerValue import AnswerValue
from ..serializers.AnswerValueSerializer import AnswerValueSerializer


class AnswerValueView(ModelViewSet):
    queryset = AnswerValue.objects.all()
    permission_classes = (DjModelPermForDRF,)
    serializer_class = AnswerValueSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('question',)
    ordering = ('id',)
