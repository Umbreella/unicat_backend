from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import ModelSerializer

from ..models import User


class UserSerializer(ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'first_name', 'last_name', 'photo',
            'is_staff', 'groups', 'user_permissions',
        )
