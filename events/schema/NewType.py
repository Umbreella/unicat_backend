import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from ..models.New import New


class NewType(DjangoObjectType):
    author = graphene.String()

    class Meta:
        model = New
        interfaces = (relay.Node, )
        fields = "__all__"

    def resolve_preview(self, info):
        return info.context.build_absolute_uri(self.preview.url)

    def resolve_author(self, info):
        return f'{self.author}'


class NewsConnection(relay.Connection):
    class Meta:
        node = NewType


class NewsQuery(graphene.ObjectType):
    new = relay.Node.Field(NewType)
    all_news = relay.ConnectionField(NewsConnection)

    def resolve_all_news(root, info, **kwargs):
        return New.objects.all()
