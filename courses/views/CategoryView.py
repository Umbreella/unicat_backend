from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ..models.Category import Category
from ..serializers.CategorySerializer import CategorySerializer


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('title',)
    ordering_fields = '__all__'
    ordering = ('id',)
