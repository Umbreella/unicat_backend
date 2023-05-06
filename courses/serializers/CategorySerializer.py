from rest_framework.serializers import ModelSerializer

from ..models.Category import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title',)
