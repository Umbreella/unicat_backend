from rest_framework.serializers import ModelSerializer

from ..models.Course import Course


class ListCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'id', 'title', 'price', 'count_lectures', 'count_independents',
        )
