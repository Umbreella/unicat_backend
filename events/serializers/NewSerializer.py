from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import ModelSerializer

from ..models.New import New


class NewSerializer(ModelSerializer):
    preview = Base64ImageField(required=False)

    class Meta:
        model = New
        fields = (
            'id', 'preview', 'title', 'short_description', 'description',
            'author', 'created_at',
        )
