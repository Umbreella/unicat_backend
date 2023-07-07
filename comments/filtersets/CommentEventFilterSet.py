from django_filters import CharFilter
from graphql import GraphQLError
from graphql_relay import from_global_id

from events.schema.EventType import EventType

from ..models.CommentedTypeChoices import CommentedTypeChoices
from .CommentFilterSet import CommentFilterSet


class CommentEventFilterSet(CommentFilterSet):
    event_id = CharFilter(method='event_comments')

    def event_comments(self, queryset, name, value):
        type_, event_id = from_global_id(value)

        if type_ != EventType.__name__:
            raise GraphQLError('event_id: not valid value.')

        lookup = {
            'commented_type': CommentedTypeChoices.EVENT.value,
            'commented_id': event_id,
        }

        return queryset.filter(**lookup)
