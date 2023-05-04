from ..serializers.CreateCommentEventSerializer import \
    CreateCommentEventSerializer
from .CreateCommentView import CreateCommentView


class CreateCommentEventView(CreateCommentView):
    serializer_class = CreateCommentEventSerializer
