from django.contrib.auth.models import Permission
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF

from ..serializers.PermissionSerializer import PermissionSerializer


class PermissionView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Permission.objects.all()
    permission_classes = (DjModelPermForDRF,)
    serializer_class = PermissionSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
