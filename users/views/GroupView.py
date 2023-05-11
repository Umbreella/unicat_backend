from django.contrib.auth.models import Group
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ..serializers.GroupSerializer import GroupSerializer


class GroupView(ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = GroupSerializer
    filter_backends = (OrderingFilter,)
    ordering = ('id',)
