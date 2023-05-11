from rest_framework.serializers import CharField, ModelSerializer

from ..models.Teacher import Teacher


class ListTeacherSerializer(ModelSerializer):
    user = CharField()

    class Meta:
        model = Teacher
        fields = (
            'id', 'user', 'description',
        )
