from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ..models import User
from ..serializers.ListUserSerializer import ListUserSerializer
from ..serializers.UserSerializer import UserSerializer


class UserView(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    filter_backends = (SearchFilter, OrderingFilter,)
    ordering_fields = '__all__'
    ordering = ('id',)

    def list(self, request, *args, **kwargs):
        self.serializer_class = ListUserSerializer
        return super().list(self, request, *args, **kwargs)
