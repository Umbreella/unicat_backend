from rest_framework.serializers import ModelSerializer

from ..models.Event import Event


class ListEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id', 'title', 'date', 'start_time', 'end_time', 'place',
        )
