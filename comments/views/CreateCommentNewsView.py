from ..serializers.CreateCommentNewsSerializer import \
    CreateCommentNewsSerializer
from .CreateCommentView import CreateCommentView


class CreateCommentNewsView(CreateCommentView):
    serializer_class = CreateCommentNewsSerializer
