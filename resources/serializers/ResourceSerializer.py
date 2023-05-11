from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import ModelSerializer

from ..models.Resource import Resource


class ResourceSerializer(ModelSerializer):
    file = Base64ImageField()

    class Meta:
        model = Resource
        fields = (
            'id', 'name', 'file', 'loaded_at',
        )
