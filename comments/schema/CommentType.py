import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField as DjFConnection

from users.schema.UserType import UserType

from ..filtersets.CommentCourseFilterSet import CommentCourseFilterSet
from ..filtersets.CommentEventFilterSet import CommentEventFilterSet
from ..filtersets.CommentNewsFilterSet import CommentNewsFilterSet
from ..models.Comment import Comment


class CountableConnectionBase(relay.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()


class CommentType(DjangoObjectType):
    author = graphene.Field(UserType)
    created_at = graphene.String()

    class Meta:
        model = Comment
        interfaces = (relay.Node,)
        fields = (
            'id', 'author', 'body', 'created_at', 'rating',
        )
        connection_class = CountableConnectionBase

    def resolve_author(self, info):
        return info.context.loaders.user_loader.load(self.author_id)

    def resolve_created_at(self, info):
        return self.created_at.strftime('%d.%m.%Y')


class CommentQuery(graphene.ObjectType):
    all_course_comments = DjFConnection(CommentType,
                                        filterset_class=CommentCourseFilterSet)
    all_news_comments = DjFConnection(CommentType,
                                      filterset_class=CommentNewsFilterSet)
    all_event_comments = DjFConnection(CommentType,
                                       filterset_class=CommentEventFilterSet)
