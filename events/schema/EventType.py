import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from ..models.Event import Event


class EventType(DjangoObjectType):
    created_at = graphene.String()

    class Meta:
        model = Event
        interfaces = (relay.Node, )
        fields = "__all__"

    def resolve_preview(self, info):
        return info.context.build_absolute_uri(self.preview.url)

    def resolve_created_at(self, info):
        return self.created_at.strftime("%d.%m.%Y")


class EventsConnection(relay.Connection):
    class Meta:
        node = EventType


class EventQuery(graphene.ObjectType):
    event = relay.Node.Field(EventType)
    all_events = relay.ConnectionField(EventsConnection)

    def resolve_all_events(root, info, **kwargs):
        return Event.objects.all().order_by('-created_at')
