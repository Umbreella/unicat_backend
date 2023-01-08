from rest_framework import serializers

from unicat.graphql.functions import get_id_from_value

from ..models.Comment import Comment
from ..models.CommentedType import CommentedType
from .CommentSerializer import CommentSerializer


class CommentCourseSerializer(CommentSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    def create(self, validated_data):
        data = validated_data
        data.update({
            'author': self.context.get('user'),
            'commented_type': CommentedType.COURSE.value,
            'commented_id': get_id_from_value(data['commented_id'])
        })

        self.comment = Comment.objects.create(**data)

        return self.comment
