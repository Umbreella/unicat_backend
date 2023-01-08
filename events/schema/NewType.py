import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from ..models.New import New


class NewType(DjangoObjectType):
    author = graphene.String()
    created_at = graphene.String()

    class Meta:
        model = New
        interfaces = (relay.Node,)
        fields = "__all__"

    def resolve_preview(self, info):
        return info.context.build_absolute_uri(self.preview.url)

    def resolve_created_at(self, info):
        return self.created_at.strftime("%d.%m.%Y")


class NewsConnection(relay.Connection):
    class Meta:
        node = NewType


class NewsQuery(graphene.ObjectType):
    news = relay.Node.Field(NewType)
    all_news = relay.ConnectionField(NewsConnection)

    def resolve_all_news(root, info, **kwargs):
        return New.objects.all().order_by('-created_at')
