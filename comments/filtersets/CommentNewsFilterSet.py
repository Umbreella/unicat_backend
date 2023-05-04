from django_filters import CharFilter
from graphql import GraphQLError

from events.schema.NewType import NewType
from unicat.graphql.functions import get_id_from_value

from ..models.CommentedTypeChoices import CommentedTypeChoices
from .CommentFilterSet import CommentFilterSet


class CommentNewsFilterSet(CommentFilterSet):
    news_id = CharFilter(method='news_comments')

    def news_comments(self, queryset, name, value):
        try:
            news_id = get_id_from_value(NewType, value)
        except Exception as ex:
            detail = f'news_id: {ex}'
            raise GraphQLError(detail)

        lookup = {
            'commented_type': CommentedTypeChoices.NEWS.value,
            'commented_id': news_id,
        }

        return queryset.filter(**lookup)
