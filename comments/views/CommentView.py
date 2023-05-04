from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ..models.Comment import Comment
from ..serializers.CommentSerializer import CommentSerializer


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('commented_type',)
    ordering = ('-id',)
    ordering_fields = ('id',)
