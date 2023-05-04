from ..serializers.CreateCommentCourseSerializer import \
    CreateCommentCourseSerializer
from .CreateCommentView import CreateCommentView


class CreateCommentCourseView(CreateCommentView):
    serializer_class = CreateCommentCourseSerializer
