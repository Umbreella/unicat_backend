from django_filters import CharFilter
from graphql import GraphQLError
from graphql_relay import from_global_id

from events.schema.NewType import NewType

from ..models.CommentedTypeChoices import CommentedTypeChoices
from .CommentFilterSet import CommentFilterSet


class CommentNewsFilterSet(CommentFilterSet):
    news_id = CharFilter(method='news_comments')

    def news_comments(self, queryset, name, value):
        type_, news_id = from_global_id(value)

        if type_ != NewType.__name__:
            raise GraphQLError('news_id: not valid value.')

        lookup = {
            'commented_type': CommentedTypeChoices.NEWS.value,
            'commented_id': news_id,
        }

        return queryset.filter(**lookup)
