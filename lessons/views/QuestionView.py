from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF

from ..models.Question import Question
from ..serializers.QuestionSerializer import QuestionSerializer


class QuestionView(ModelViewSet):
    queryset = Question.objects.all()
    permission_classes = (DjModelPermForDRF,)
    serializer_class = QuestionSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('lesson_id',)
    ordering = ('id',)
