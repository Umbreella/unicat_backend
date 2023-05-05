from rest_framework.serializers import ModelSerializer

from ..models.New import New


class ListNewSerializer(ModelSerializer):
    class Meta:
        model = New
        fields = (
            'id', 'title', 'created_at',
        )
