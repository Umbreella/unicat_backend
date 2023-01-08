from ..serializers.CommentEventSerializer import CommentEventSerializer
from .CommentView import CommentView


class CommentEventView(CommentView):
    serializer_class = CommentEventSerializer
