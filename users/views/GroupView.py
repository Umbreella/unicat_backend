from django.contrib.auth.models import Group
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF

from ..serializers.GroupSerializer import GroupSerializer


class GroupView(ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = (DjModelPermForDRF,)
    serializer_class = GroupSerializer
    filter_backends = (OrderingFilter,)
    ordering = ('id',)
