from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import ModelSerializer

from ..models.Event import Event


class EventSerializer(ModelSerializer):
    preview = Base64ImageField(required=False)

    class Meta:
        model = Event
        fields = (
            'id', 'preview', 'title', 'short_description', 'description',
            'date', 'start_time', 'end_time', 'place', 'created_at',
        )
