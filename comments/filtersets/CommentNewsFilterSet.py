from django_filters import CharFilter

from unicat.graphql.functions import get_id_from_value

from ..models.CommentedType import CommentedType
from .CommentFilterSet import CommentFilterSet


class CommentNewsFilterSet(CommentFilterSet):
    news_id = CharFilter(method='news_comments')

    def news_comments(self, queryset, name, value):
        news_id = get_id_from_value(value)

        lookup = {
            'commented_type': CommentedType.NEWS.value,
            'commented_id': news_id
        }

        return queryset.filter(**lookup)
