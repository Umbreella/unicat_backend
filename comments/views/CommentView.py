from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF

from ..models.Comment import Comment
from ..serializers.CommentSerializer import CommentSerializer


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = (DjModelPermForDRF,)
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('commented_type',)
    ordering = ('-id',)
    ordering_fields = ('id',)
