from rest_framework.serializers import ModelSerializer

from ..models.Teacher import Teacher


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = (
            'id', 'user', 'description', 'facebook', 'twitter', 'google_plus',
            'vk',
        )
