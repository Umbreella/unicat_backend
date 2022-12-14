import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from ..models.Event import Event


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        interfaces = (relay.Node, )
        fields = "__all__"

    def resolve_preview(self, info):
        return info.context.build_absolute_uri(self.preview.url)


class EventsConnection(relay.Connection):
    class Meta:
        node = EventType


class EventQuery(graphene.ObjectType):
    event = relay.Node.Field(EventType)
    all_events = relay.ConnectionField(EventsConnection)

    def resolve_all_events(root, info, **kwargs):
        return Event.objects.all()
