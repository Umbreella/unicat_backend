import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField as DjFConnection

from users.schema.UserType import UserType

from ..filtersets.CommentCourseFilterSet import CommentCourseFilterSet
from ..filtersets.CommentEventFilterSet import CommentEventFilterSet
from ..filtersets.CommentNewsFilterSet import CommentNewsFilterSet
from ..models.Comment import Comment


class CommentType(DjangoObjectType):
    author = graphene.Field(UserType)
    created_at = graphene.String()

    class Meta:
        model = Comment
        interfaces = (relay.Node,)
        fields = '__all__'

    def resolve_created_at(self, info):
        return self.created_at.strftime("%d.%m.%Y")


class CommentQuery(graphene.ObjectType):
    all_course_comments = DjFConnection(CommentType,
                                        filterset_class=CommentCourseFilterSet)
    all_news_comments = DjFConnection(CommentType,
                                      filterset_class=CommentNewsFilterSet)
    all_event_comments = DjFConnection(CommentType,
                                       filterset_class=CommentEventFilterSet)
