from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ..models.Question import Question
from ..serializers.QuestionSerializer import QuestionSerializer


class QuestionView(ModelViewSet):
    queryset = Question.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = QuestionSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('lesson_id',)
    ordering = ('id',)
