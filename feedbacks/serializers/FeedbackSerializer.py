from rest_framework.serializers import ModelSerializer

from ..models.Feedback import Feedback


class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = (
            'id', 'name', 'email', 'body', 'created_at', 'is_closed',
        )
