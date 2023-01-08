from django_filters import CharFilter

from unicat.graphql.functions import get_id_from_value

from ..models.CommentedType import CommentedType
from .CommentFilterSet import CommentFilterSet


class CommentEventFilterSet(CommentFilterSet):
    event_id = CharFilter(method='event_comments')

    def event_comments(self, queryset, name, value):
        event_id = get_id_from_value(value)

        lookup = {
            'commented_type': CommentedType.EVENT.value,
            'commented_id': event_id
        }

        return queryset.filter(**lookup)
