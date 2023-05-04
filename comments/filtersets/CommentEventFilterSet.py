from django_filters import CharFilter
from graphql import GraphQLError

from events.schema.EventType import EventType
from unicat.graphql.functions import get_id_from_value

from ..models.CommentedTypeChoices import CommentedTypeChoices
from .CommentFilterSet import CommentFilterSet


class CommentEventFilterSet(CommentFilterSet):
    event_id = CharFilter(method='event_comments')

    def event_comments(self, queryset, name, value):
        try:
            event_id = get_id_from_value(EventType, value)
        except Exception as ex:
            detail = f'event_id: {ex}'
            raise GraphQLError(detail)

        lookup = {
            'commented_type': CommentedTypeChoices.EVENT.value,
            'commented_id': event_id,
        }

        return queryset.filter(**lookup)
