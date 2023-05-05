from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ..models.New import New
from ..serializers.ListNewSerializer import ListNewSerializer
from ..serializers.NewSerializer import NewSerializer


class NewView(ModelViewSet):
    queryset = New.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = NewSerializer
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('title',)
    # ordering_fields = '__all__'
    ordering = ('id',)

    def list(self, request, *args, **kwargs):
        self.serializer_class = ListNewSerializer
        return super().list(self, request, *args, **kwargs)
