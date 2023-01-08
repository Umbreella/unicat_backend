from ..serializers.CommentNewsSerializer import CommentNewsSerializer
from .CommentView import CommentView


class CommentNewsView(CommentView):
    serializer_class = CommentNewsSerializer
