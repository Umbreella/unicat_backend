from rest_framework import serializers


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    body = serializers.CharField()
    createdAt = serializers.DateTimeField(source='created_at',
                                          format="%d-%m-%Y", read_only=True)
    countLike = serializers.IntegerField(source='count_like', read_only=True)
    commented_id = serializers.CharField(max_length=255, write_only=True)
    author = serializers.CharField(read_only=True)
