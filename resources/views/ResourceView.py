from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF

from ..models.Resource import Resource
from ..serializers.ResourceSerializer import ResourceSerializer


class ResourceView(ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = (DjModelPermForDRF,)
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = '__all__'
    ordering = ('id',)
