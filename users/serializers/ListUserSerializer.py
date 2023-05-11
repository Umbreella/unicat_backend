from rest_framework.serializers import ModelSerializer

from ..models import User


class ListUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'is_staff',
        )
