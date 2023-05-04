from rest_framework.serializers import ModelSerializer

from ..models.Comment import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'body', 'created_at',)
