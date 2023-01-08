from ..serializers.CommentCourseSerializer import CommentCourseSerializer
from .CommentView import CommentView


class CommentCourseView(CommentView):
    serializer_class = CommentCourseSerializer
