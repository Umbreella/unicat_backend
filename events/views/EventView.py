from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF

from ..models.Event import Event
from ..serializers.EventSerializer import EventSerializer
from ..serializers.ListEventSerializer import ListEventSerializer


class EventView(ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = (DjModelPermForDRF,)
    serializer_class = EventSerializer
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('title',)
    ordering = ('id',)

    def list(self, request, *args, **kwargs):
        self.serializer_class = ListEventSerializer
        return super().list(self, request, *args, **kwargs)
