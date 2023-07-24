import copy

from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF

from ..models.New import New
from ..serializers.ListNewSerializer import ListNewSerializer
from ..serializers.NewSerializer import NewSerializer


class NewView(ModelViewSet):
    queryset = New.objects.all()
    permission_classes = (DjModelPermForDRF,)
    serializer_class = NewSerializer
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('title',)
    ordering_fields = '__all__'
    ordering = ('id',)

    def list(self, request, *args, **kwargs):
        self.serializer_class = ListNewSerializer
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = copy.copy(request.data)
        data.update({
            'author': request.user.id,
        })

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
